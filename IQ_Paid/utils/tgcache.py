import asyncio
import json
import os
import requests
import yt_dlp
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from IQ_Paid import app, userbot, LOGGER
from config import TG_SONGS_STORAGE, TG_INDEX_CHANNEL, YT_API_KEY, YTPROXY_URL as YTPROXY, YT_API_KEY2, YTPROXY_URL2 as YTPROXY2

logger = LOGGER(__name__)

# Memory cache
_memory_cache = {}


def create_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.1)
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


async def download_with_requests(url, filepath):
    try:
        session = create_session()
        response = session.get(url, stream=True, timeout=60, allow_redirects=True)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        return filepath
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return None
    finally:
        session.close()


async def search_index(video_id: str) -> dict:
    try:
        async for message in userbot.one.search_messages(int(TG_INDEX_CHANNEL), video_id):
            if message.text:
                try:
                    data = json.loads(message.text)
                    if data.get("video_id") == video_id:
                        return data
                except:
                    continue
    except Exception as e:
        logger.error(f"Index search error: {str(e)}")
    return {}


async def save_index(video_id: str, audio_file_id: str = None, video_file_id: str = None):
    try:
        existing = await search_index(video_id)
        if existing:
            audio_file_id = audio_file_id or existing.get("audio_file_id")
            video_file_id = video_file_id or existing.get("video_file_id")
        data = {
            "video_id": video_id,
            "audio_file_id": audio_file_id,
            "video_file_id": video_file_id
        }
        await app.send_message(int(TG_INDEX_CHANNEL), json.dumps(data))
        logger.info(f"Index saved: {video_id}")
        return data
    except Exception as e:
        logger.error(f"Save index error: {str(e)}")
        return {}


async def upload_audio_to_tg(video_id: str, filepath: str) -> str:
    try:
        msg = await app.send_audio(
            int(TG_SONGS_STORAGE),
            audio=filepath,
            caption=f"🎵 Audio | {video_id}"
        )
        if msg and msg.audio:
            logger.info(f"Audio uploaded to TG: {video_id}")
            return msg.audio.file_id
    except Exception as e:
        logger.error(f"Audio upload error: {str(e)}")
    return None


async def upload_video_to_tg(video_id: str, filepath: str) -> str:
    try:
        msg = await app.send_video(
            int(TG_SONGS_STORAGE),
            video=filepath,
            caption=f"🎬 Video | {video_id}"
        )
        if msg and msg.video:
            logger.info(f"Video uploaded to TG: {video_id}")
            return msg.video.file_id
    except Exception as e:
        logger.error(f"Video upload error: {str(e)}")
    return None


async def get_audio(video_id: str, cookie_file: str = None) -> str:
    try:
        # 1. Memory cache check
        if video_id in _memory_cache and _memory_cache[video_id].get("audio"):
            fp = _memory_cache[video_id]["audio"]
            if os.path.exists(fp):
                logger.info(f"Memory cache hit audio: {video_id}")
                return fp

        # 2. VPS file check
        filepath = os.path.join("downloads", f"{video_id}.mp3")
        if os.path.exists(filepath):
            logger.info(f"VPS cache hit audio: {video_id}")
            _memory_cache.setdefault(video_id, {})["audio"] = filepath
            return filepath

        # 3. xBit API - download to VPS
        if YT_API_KEY and YTPROXY:
            try:
                session = create_session()
                headers = {"x-api-key": YT_API_KEY, "User-Agent": "Mozilla/5.0"}
                resp = session.get(f"{YTPROXY}/info/{video_id}", headers=headers, timeout=60)
                data = resp.json()
                session.close()
                if data.get("status") == "success":
                    audio_url = data.get("audio_url")
                    if audio_url:
                        result = await download_with_requests(audio_url, filepath)
                        if result:
                            logger.info(f"xBit audio downloaded: {video_id}")
                            _memory_cache.setdefault(video_id, {})["audio"] = filepath
                            async def bg_upload_xbit_audio():
                                try:
                                    file_id = await upload_audio_to_tg(video_id, filepath)
                                    if file_id:
                                        await save_index(video_id, audio_file_id=file_id)
                                        logger.info(f"BG audio upload done: {video_id}")
                                except Exception as e:
                                    logger.error(f"BG audio upload error: {str(e)}")
                            asyncio.create_task(bg_upload_xbit_audio())
                            return filepath
            except Exception as e:
                logger.error(f"xBit audio failed: {str(e)}")

        # 4. yt-dlp + cookies fallback
        if cookie_file:
            try:
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": f"downloads/{video_id}.%(ext)s",
                    "geo_bypass": True,
                    "nocheckcertificate": True,
                    "quiet": True,
                    "no_warnings": True,
                    "cookiefile": cookie_file,
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                }
                x = yt_dlp.YoutubeDL(ydl_opts)
                x.download([f"https://www.youtube.com/watch?v={video_id}"])
                if os.path.exists(filepath):
                    logger.info(f"yt-dlp audio downloaded: {video_id}")
                    _memory_cache.setdefault(video_id, {})["audio"] = filepath
                    async def bg_upload_ytdlp_audio():
                        try:
                            file_id = await upload_audio_to_tg(video_id, filepath)
                            if file_id:
                                await save_index(video_id, audio_file_id=file_id)
                                logger.info(f"BG audio upload done: {video_id}")
                        except Exception as e:
                            logger.error(f"BG audio upload error: {str(e)}")
                    asyncio.create_task(bg_upload_ytdlp_audio())
                    return filepath
            except Exception as e:
                logger.error(f"yt-dlp audio failed: {str(e)}")

        # 5. BabyAPI fallback - direct stream
        if YT_API_KEY2 and YTPROXY2:
            try:
                session = create_session()
                url = f"{YTPROXY2}/api/song?query={video_id}&api={YT_API_KEY2}"
                resp = session.get(url, timeout=60)
                data = resp.json()
                session.close()
                stream_url = data.get("stream")
                if stream_url:
                    logger.info(f"BabyAPI audio stream: {video_id}")
                    return stream_url
            except Exception as e:
                logger.error(f"BabyAPI audio failed: {str(e)}")

    except Exception as e:
        logger.error(f"get_audio error: {str(e)}")
    return None


async def get_video(video_id: str, cookie_file: str = None) -> str:
    try:
        # 1. Memory cache check
        if video_id in _memory_cache and _memory_cache[video_id].get("video"):
            fp = _memory_cache[video_id]["video"]
            if os.path.exists(fp):
                logger.info(f"Memory cache hit video: {video_id}")
                return fp

        # 2. VPS file check
        filepath = os.path.join("downloads", f"{video_id}.mp4")
        if os.path.exists(filepath):
            logger.info(f"VPS cache hit video: {video_id}")
            _memory_cache.setdefault(video_id, {})["video"] = filepath
            return filepath

        # 3. yt-dlp 720p + cookies
        if cookie_file:
            try:
                # 24hr cleanup
                import time
                now = time.time()
                for f in os.listdir("downloads"):
                    fpath = os.path.join("downloads", f)
                    if os.path.isfile(fpath) and now - os.path.getmtime(fpath) > 86400:
                        os.remove(fpath)
            except:
                pass
            try:
                ydl_opts = {
                    "format": "bestvideo[height<=720][ext=mp4]+bestaudio/best",
                    "outtmpl": f"downloads/{video_id}.%(ext)s",
                    "merge_output_format": "mp4",
                    "geo_bypass": True,
                    "nocheckcertificate": True,
                    "quiet": True,
                    "no_warnings": True,
                    "cookiefile": cookie_file,
                }
                x = yt_dlp.YoutubeDL(ydl_opts)
                x.download([f"https://www.youtube.com/watch?v={video_id}"])
                if os.path.exists(filepath):
                    logger.info(f"yt-dlp 720p video downloaded: {video_id}")
                    _memory_cache.setdefault(video_id, {})["video"] = filepath
                    async def bg_upload_video():
                        try:
                            file_id = await upload_video_to_tg(video_id, filepath)
                            if file_id:
                                await save_index(video_id, video_file_id=file_id)
                                logger.info(f"BG video upload done: {video_id}")
                        except Exception as e:
                            logger.error(f"BG video upload error: {str(e)}")
                    asyncio.create_task(bg_upload_video())
                    return filepath
            except Exception as e:
                logger.error(f"yt-dlp video failed: {str(e)}")

        # 4. xBit fallback - direct stream
        if YT_API_KEY and YTPROXY:
            try:
                session = create_session()
                headers = {"x-api-key": YT_API_KEY, "User-Agent": "Mozilla/5.0"}
                resp = session.get(f"{YTPROXY}/info/{video_id}", headers=headers, timeout=60)
                data = resp.json()
                session.close()
                if data.get("status") == "success":
                    video_url = data.get("video_url")
                    if video_url:
                        logger.info(f"xBit video fallback: {video_id}")
                        return video_url
            except Exception as e:
                logger.error(f"xBit video failed: {str(e)}")

    except Exception as e:
        logger.error(f"get_video error: {str(e)}")
    return None
