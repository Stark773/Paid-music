# ========================================================
import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters
load_dotenv()
# ======================================================
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
# ======================================================
OWNER_ID = int(getenv("OWNER_ID", "7875184322"))
OWNER_USERNAME = getenv("OWNER_USERNAME", "YourUsername")
BOT_USERNAME = getenv("BOT_USERNAME", "Muskan_Music_Bot")
BOT_NAME = "Muskan Music"
ASSUSERNAME = getenv("ASSUSERNAME")
# ======================================================
MONGO_DB_URI = getenv("MONGO_DB_URI", "")
LOGGER_ID = int(getenv("LOGGER_ID", "-100"))
# ======================================================
BASE_URL = getenv("BASE_URL", "https://BabyAPI.Pro")
API_KEY = getenv("API_KEY", None)
# ======================================================
TG_SONGS_STORAGE = getenv("TG_SONGS_STORAGE", "")
TG_INDEX_CHANNEL = getenv("TG_INDEX_CHANNEL", "")
# ======================================================
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT_MIN", "17000"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))
# ======================================================
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("AUTO_LEAVE_ASSISTANT_TIME", "300"))
# ======================================================
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
# ======================================================
UPSTREAM_REPO = "https://github.com/Stark773/Paid-music"
UPSTREAM_BRANCH = "main"
GIT_TOKEN = getenv("GIT_TOKEN", None)
# ======================================================
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/muskan_music_official")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/muskan_music_support")
# ======================================================
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "")
# ======================================================
STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")
STRING6 = getenv("STRING_SESSION6")
STRING7 = getenv("STRING_SESSION7")
# ======================================================
START_IMG_URL = getenv("START_IMG_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg")
# ======================================================
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
# ======================================================
def time_to_seconds(time: str) -> int:
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))
DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
# ======================================================
if SUPPORT_CHANNEL and not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHANNEL URL. Must start with https://")
if SUPPORT_CHAT and not re.match(r"(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHAT URL. Must start with https://")
