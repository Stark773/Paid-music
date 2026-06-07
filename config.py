# ========================================================
import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters
load_dotenv()
# ======================================================
API_ID = int(getenv("API_ID", "39917988"))
API_HASH = getenv("API_HASH", "bd827dbeac6a55896ff11539bc80365b")
BOT_TOKEN = getenv("BOT_TOKEN", "8522799922:AAELRX3i7EzN9nCeQa_6x4BhgJKo6Z9V55w")
# ======================================================
OWNER_ID = int(getenv("OWNER_ID", "7875184322"))
OWNER_USERNAME = "Itzz_Istkhar"
BOT_USERNAME = "Sukku_Music_Bot"
BOT_NAME = "Sonali Music"
ASSUSERNAME = getenv("ASSUSERNAME")
# ======================================================
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://marin:marin69@cluster0.zxaf7uc.mongodb.net/?retryWrites=true&w=majority")
LOGGER_ID = int(getenv("LOGGER_ID", "-1003781924669"))
# ======================================================
YTPROXY_URL = 'https://tgapi.xbitcode.com'
YT_API_KEY = 'xbit_DSsv0UVt9GVmGSTN5RViq7i-u4qHyFJK'
YTPROXY_URL2 = 'https://BabyAPI.Pro'
YT_API_KEY2 = 'ADMINBABYX1C073D754502E7A7D0305725EC0E41F5'
# ======================================================
TG_SONGS_STORAGE = "-1003947409698"
TG_INDEX_CHANNEL = "-1003719552350"
# ======================================================
DURATION_LIMIT_MIN = int(17000)
SONG_DOWNLOAD_DURATION = int("9999999")
SONG_DOWNLOAD_DURATION_LIMIT = int("9999999")
PLAYLIST_FETCH_LIMIT = int(25)
TG_AUDIO_FILESIZE_LIMIT = int("5242880000")
TG_VIDEO_FILESIZE_LIMIT = int("5242880000")
# ======================================================
AUTO_LEAVING_ASSISTANT = "True"
AUTO_LEAVE_ASSISTANT_TIME = int("300")
# ======================================================
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
# ======================================================
UPSTREAM_REPO = "https://github.com/BabiesIQ/PAID"
UPSTREAM_BRANCH = "main"
GIT_TOKEN = None
# ======================================================
SUPPORT_CHANNEL = "https://t.me/+8WjqAqBihwkyNzk9"
SUPPORT_CHAT = "https://t.me/+8WjqAqBihwkyNzk9"
# ======================================================
SPOTIFY_CLIENT_ID = "1c21247d714244ddbb09925dac565aed"
SPOTIFY_CLIENT_SECRET = "709e1a2969664491b58200860623ef19"
# ======================================================
STRING1 = getenv("STRING_SESSION", "BQJhGaQAJr35OSSAAo_gx0MvYKjl9E6LMm9FYU7e8I6bMc3te62ig3S4-VmdXoxvwHUlDigY2Fxz7i3gsvDDSOheBGa5QJaDdvPePdpOkEcoHo2AHG-ySWgmfMi283XuCCYjpoOaa_0OpMU7SVi04E7L1Go3eCkzNEtDJzkS6WmNc6lve1A5OHKVhsY76U8mAXJL6dc3iRjmbqJrVyKcfb5Sh_MNiXKy9qHzW0-kVrh0FjuViWiDj2y_LtbURTe9gzqPx2buDhTJY_c5V4CdmDGR8zzIBZaU-BLzv46o7jnn8pLRYua8oI0KB8U-BAWDlgE18WyXmb4XBZpw6H0y2FJKx3aDhQAAAAHVZcbCAA")
STRING2 = None
STRING3 = None
STRING4 = None
STRING5 = None
STRING6 = None
STRING7 = None
# ======================================================
START_IMG_URL = "https://files.catbox.moe/x5lytj.jpg"
PING_IMG_URL = "https://files.catbox.moe/leaexg.jpg"
PLAYLIST_IMG_URL = "https://files.catbox.moe/b0e4vk.jpg"
STATS_IMG_URL = "https://files.catbox.moe/psya34.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/4dzp6n.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/4dzp6n.jpg"
STREAM_IMG_URL = "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/4dzp6n.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/4dzp6n.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/2y5o3g.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/2y5o3g.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg"
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
    raise SystemExit(
        "[ERROR] - Invalid SUPPORT_CHANNEL URL. It must start with https://"
    )
if SUPPORT_CHAT and not re.match(r"(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit(
        "[ERROR] - Invalid SUPPORT_CHAT URL. It must start with https://"
    )
