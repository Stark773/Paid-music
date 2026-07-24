import asyncio
import os
import re
import json
from typing import Union
import requests
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from py_yt import VideosSearch
from Muskan.utils.database import is_on_off
from Muskan.utils.formatters import time_to_seconds
import glob
import random
import aiohttp
import config
from config import LOGGER_ID
from Muskan import app
from config import BASE_URL, API_KEY
from urllib.parse import urlparse

STREAM_MODE = False  # True = download local | False = direct stream from API


def safe_yt_shell(url: str) -> bool:
    try:
        p = urlparse(url)
        if p.scheme not in ("http", "https"):
            return False
        allowed = ("youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be")
        if not any(domain in p.netloc for domain in allowed):
            return False
        if any(x in url for x in [";", "|", "$", "`", "\n", "\r"]):
            return False
        return True
    except Exception:
        return False


def cookie_txt_file():
    cookie_dir = f"{os.getcwd()}/cookies"
    if not os.path.exists(cookie_dir):
        return None
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
    if not cookies_files:
        return None
    return os.path.join(cookie_dir, random.choice(cookies_files))


async def _download_media(link: str, kind: str, exts: list, wait: int = 60):
    vid = link.split("v=")[-1].split("&")[0]
    os.makedirs("downloads", exist_ok=True)
    try:
        if not STREAM_MODE:
            if kind == "song":
                voice_path = f"downloads/{vid}.voice.ogg"
                if os.path.exists(voice_path) and os.path.getsize(voice_path) > 1000:
                    return voice_path
            for e in exts:
                p = f"downloads/{vid}.{e}"
                if os.path.exists(p):
                    return await _prepare_audio_for_call(p) if kind == "song" else p
        async with aiohttp.ClientSession() as s:
            url = (
                f"{BASE_URL}/api/{kind}?query={vid}&api={API_KEY}"
                if STREAM_MODE
                else f"{BASE_URL}/api/{kind}?query={vid}&download=true&api={API_KEY}"
            )
            async with s.get(url) as r:
                j = await r.json()
            u = j.get("stream")
            if not u:
                raise Exception("no stream")
            if j.get("type") == "live":
                return u
            for _ in range(wait):
                async with s.get(u, allow_redirects=False) as r:
                    if r.status in (200, 206, 301, 302):
                        break
                    if r.status in (204, 423, 404, 410):
                        await asyncio.sleep(2)
                        continue
                    if r.status in (401, 403, 429):
                        raise Exception(f"block {r.status}")
                    raise Exception(f"fail {r.status}")
            else:
                raise Exception("timeout")
            if STREAM_MODE:
                return u
            p = f"downloads/{vid}.{'mp3' if kind == 'song' else 'mp4'}"
            part_path = f"{p}.part"
            proc = await asyncio.create_subprocess_exec(
                "curl",
                "-L",
                "--fail",
                "--silent",
                "--show-error",
                "--retry",
                "3",
                "--connect-timeout",
                "20",
                "--max-time",
                "120",
                "-o",
                part_path,
                "-w",
                "%{http_code}",
                u,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            http_code = stdout.decode().strip() if stdout else "?"
            if proc.returncode != 0:
                try:
                    os.remove(part_path)
                except FileNotFoundError:
                    pass
                error = stderr.decode("utf-8", "replace").strip() or f"curl exit {proc.returncode}"
                raise Exception(f"download failed ({http_code}): {error[:120]}")
            os.replace(part_path, p)
            size = os.path.getsize(p) if os.path.exists(p) else 0
            # Read first 16 bytes to check if it's actually audio
            magic = b""
            if os.path.exists(p):
                with open(p, "rb") as f:
                    magic = f.read(16)
            is_audio = (
                magic[:3] == b"ID3"                        # MP3 with ID3 tag
                or magic[:2] in (b"\xff\xfb", b"\xff\xfa", b"\xff\xf3", b"\xff\xf2")  # raw MP3
                or magic[4:8] == b"ftyp"                   # M4A/MP4
                or magic[:4] in (b"OggS", b"fLaC", b"RIFF")  # OGG/FLAC/WAV
            )
            await app.send_message(
                LOGGER_ID,
                f"📥 {kind.upper()} DL\n🔗 `{link}`\n"
                f"📊 HTTP={http_code} size={size} audio={is_audio}\n"
                f"🔮 magic=`{magic[:8].hex()}`",
            )
            if not os.path.exists(p) or size < 50000:
                raise Exception(f"dl fail size={size}")
            if kind == "song" and not await _has_audio_stream(p):
                raise Exception(f"not audio magic={magic[:8].hex()}")
            return await _prepare_audio_for_call(p) if kind == "song" else p
    except Exception as e:
        await app.send_message(
            LOGGER_ID,
            f"❌ {kind.upper()} ERR\n🔗 `{link}`\n⚠️ `{str(e)[:100]}`",
        )
        raise


async def _has_audio_stream(path: str) -> bool:
    """Use ffprobe instead of file extensions/magic bytes to validate audio."""
    proc = await asyncio.create_subprocess_exec(
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=codec_type",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    return proc.returncode == 0 and "audio" in stdout.decode("utf-8", "replace").lower()


async def _prepare_audio_for_call(path: str) -> str:
    """Normalize downloaded audio to a seekable voice-chat friendly stream."""
    path = os.path.abspath(path)
    if not os.path.isfile(path) or not await _has_audio_stream(path):
        raise Exception(f"audio source is not readable: {path}")

    output = os.path.splitext(path)[0] + ".voice.ogg"
    if os.path.isfile(output) and os.path.getsize(output) > 1000:
        return output

    part_path = f"{output}.part"
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        path,
        "-map",
        "0:a:0",
        "-vn",
        "-ac",
        "2",
        "-ar",
        "48000",
        "-c:a",
        "libopus",
        "-b:a",
        "128k",
        part_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0 or not os.path.isfile(part_path) or os.path.getsize(part_path) <= 1000:
        try:
            os.remove(part_path)
        except FileNotFoundError:
            pass
        error = stderr.decode("utf-8", "replace").strip() or f"ffmpeg exit {proc.returncode}"
        raise Exception(f"audio normalization failed: {error[:160]}")
    os.replace(part_path, output)
    return output


async def download_song(link: str):
    return await _download_media(link, "song", ["mp3", "m4a", "webm"], 60)


async def download_video(link: str):
    return await _download_media(link, "video", ["mp4", "webm", "mkv"], 90)


async def check_file_size(link):
    if not safe_yt_shell(link):
        return None
    cookie_file = cookie_txt_file()
    if not cookie_file:
        return None

    async def get_format_info(link):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp", "--cookies", cookie_file, "-J", link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            return None
        return json.loads(stdout.decode())

    info = await get_format_info(link)
    if info is None:
        return None
    formats = info.get("formats", [])
    return sum(f.get("filesize", 0) for f in formats if "filesize" in f)


async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in errorz.decode("utf-8").lower():
            return out.decode("utf-8")
        return errorz.decode("utf-8")
    return out.decode("utf-8")


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset is None:
            return None
        return text[offset: offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            duration_sec = 0 if str(duration_min) == "None" else int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
        return title

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            duration = result["duration"]
        return duration

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        if not safe_yt_shell(link):
            return 0, "Invalid or unsafe URL."
        try:
            downloaded_file = await download_video(link)
            if downloaded_file:
                return 1, downloaded_file
        except Exception as e:
            print(f"BabyAPI video failed: {e}")
        cookie_file = cookie_txt_file()
        if not cookie_file:
            return 0, "No cookies found."
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp", "--cookies", cookie_file, "-g",
            "-f", "best[height<=?720][width<=?1280]", link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        return 0, stderr.decode()

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        if not safe_yt_shell(link):
            return []
        cookie_file = cookie_txt_file()
        args = ["yt-dlp", "-i", "--get-id", "--flat-playlist"]
        if cookie_file:
            args.extend(["--cookies", cookie_file])
        args.extend(["--playlist-end", str(limit), "--skip-download", link])
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        result = stdout.decode("utf-8").split("\n")
        return [k for k in result if k.strip()]

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        clean_title = title.strip()
        if len(clean_title) > 14:
            clean_title = clean_title[:14].rstrip() + "...."
        return {
            "title": clean_title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        if not safe_yt_shell(link):
            return [], link
        cookie_file = cookie_txt_file()
        if not cookie_file:
            return [], link
        ytdl_opts = {"quiet": True, "cookiefile": cookie_file}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for fmt in r["formats"]:
                try:
                    str(fmt["format"])
                except Exception:
                    continue
                if "dash" in str(fmt["format"]).lower():
                    continue
                try:
                    formats_available.append({
                        "format": fmt["format"],
                        "filesize": fmt["filesize"],
                        "format_id": fmt["format_id"],
                        "ext": fmt["ext"],
                        "format_note": fmt["format_note"],
                        "yturl": link,
                    })
                except Exception:
                    continue
        return formats_available, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link

        if not safe_yt_shell(link):
            return None, None

        vid_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link.split("/")[-1]

        if songvideo or songaudio:
            await download_song(link)
            fpath = f"downloads/{vid_id}.mp3"
            return fpath
        elif video:
            try:
                downloaded_file = await download_video(link)
                if downloaded_file:
                    return downloaded_file, True
            except Exception as e:
                print(f"BabyAPI video download failed: {e}")
            cookie_file = cookie_txt_file()
            if not cookie_file:
                return None, None
            if await is_on_off(1):
                direct = True
                downloaded_file = await download_song(link)
            else:
                proc = await asyncio.create_subprocess_exec(
                    "yt-dlp", "--cookies", cookie_file, "-g",
                    "-f", "best[height<=?720][width<=?1280]", link,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                if stdout:
                    downloaded_file = stdout.decode().split("\n")[0]
                    direct = False
                else:
                    file_size = await check_file_size(link)
                    if not file_size or file_size / (1024 * 1024) > 250:
                        return None, None
                    direct = True
                    loop = asyncio.get_running_loop()
                    def video_dl():
                        ydl_opts = {
                            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                            "outtmpl": "downloads/%(id)s.%(ext)s",
                            "geo_bypass": True,
                            "nocheckcertificate": True,
                            "quiet": True,
                            "cookiefile": cookie_file,
                            "no_warnings": True,
                        }
                        x = yt_dlp.YoutubeDL(ydl_opts)
                        info = x.extract_info(link, False)
                        xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
                        if not os.path.exists(xyz):
                            x.download([link])
                        return xyz
                    downloaded_file = await loop.run_in_executor(None, video_dl)
        else:
            direct = True
            downloaded_file = await download_song(link)

        return downloaded_file, direct
