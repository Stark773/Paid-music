<p align="center">
  <img src="https://telegra.ph/file/d30d11c4365c025c25e3e.jpg" width="300"/>
</p>

<h2 align="center">🎵 Muskan Music Bot 🎵</h2>

<p align="center">
  A powerful, feature-rich Telegram music bot with multi-platform support.
</p>

<p align="center">
  <a href="https://t.me/muskan_music_official">
    <img src="https://img.shields.io/badge/Channel-Muskan%20Music-blue?logo=telegram" alt="Channel"/>
  </a>
  <a href="https://t.me/muskan_music_support">
    <img src="https://img.shields.io/badge/Support-Group-green?logo=telegram" alt="Support"/>
  </a>
  <a href="https://github.com/Stark773/Paid-music">
    <img src="https://img.shields.io/badge/Repo-GitHub-black?logo=github" alt="Repo"/>
  </a>
</p>

---

## 🚀 Deploy to Heroku

> **Note:** Heroku one-click deploy works with public repos. If your repo is private, use the Heroku CLI (`heroku git:remote`) instead.

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Stark773/Paid-music)

---

## ✨ Features

- 🎵 High-quality audio & video streaming via **BabyAPI.Pro**
- 📋 Queue system with shuffle, loop, seek, speed control
- 🌍 Multi-language support (EN, HI, AR, PA, BN, TA, TE, ID, TR, RU, FR, DE)
- 🎨 Beautiful auto-color thumbnails
- 🎧 YouTube • Spotify • Apple Music • Resso • SoundCloud
- 📁 Telegram audio/video file support
- ⚡ Fast streaming with pytgcalls

---

## ⚙️ Required Variables

| Variable | Description |
|---|---|
| `API_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram API Hash |
| `BOT_TOKEN` | Bot token from [@BotFather](https://t.me/BotFather) |
| `MONGO_DB_URI` | MongoDB connection URI |
| `STRING_SESSION` | Pyrogram string session (assistant account) |
| `OWNER_ID` | Your Telegram user ID |
| `LOGGER_ID` | Log group/channel ID (must have active voice chat) |
| `BASE_URL` | BabyAPI base URL (default: `https://BabyAPI.Pro`) |
| `API_KEY` | Your BabyAPI key from [babyapi.pro](https://babyapi.pro) |
| `SUPPORT_CHANNEL` | Channel link e.g. `https://t.me/muskan_music_official` |
| `SUPPORT_CHAT` | Support group link e.g. `https://t.me/muskan_music_support` |

### Optional

| Variable | Description |
|---|---|
| `SPOTIFY_CLIENT_ID` | Spotify app client ID |
| `SPOTIFY_CLIENT_SECRET` | Spotify app client secret |
| `STRING_SESSION2–5` | Extra assistant sessions |
| `HEROKU_APP_NAME` | Heroku app name (for auto-restart) |
| `HEROKU_API_KEY` | Heroku API key (for auto-restart) |

---

## 🛠 Manual Setup

```bash
git clone https://github.com/Stark773/Paid-music
cd Paid-music
pip3 install -U pip
pip3 install -r requirements.txt
cp sample.env .env
# Fill in .env with your values
python3 -m Muskan
```

---

## 📜 License

© 2025–26 Muskan Music Bot. All rights reserved.
