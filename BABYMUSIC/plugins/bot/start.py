import asyncio
import random
import time
import requests
import json
import html
import traceback

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.future import VideosSearch

import config
from BABYMUSIC import app
from BABYMUSIC.misc import _boot_
from BABYMUSIC.plugins.sudo.sudoers import sudoers_list
from BABYMUSIC.utils import bot_sys_stats
from BABYMUSIC.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)
from BABYMUSIC.utils.decorators.language import LanguageStart
from BABYMUSIC.utils.formatters import get_readable_time
from BABYMUSIC.button_styles import primary_button, success_button
from BABYMUSIC.utils.inline.start import private_panel, start_panel
from BABYMUSIC.utils.inline.help import first_page
from config import BANNED_USERS, AYUV, HELP_IMG_URL, START_VIDS, STICKERS, VALID_EMOJII, EFFECT_IDS
from strings import get_string



BOT_API = f"https://api.telegram.org/bot{config.BOT_TOKEN}"


# ================= SAFE HTML HELPERS ================= #

def safe_mention(user):
    name = html.escape(user.first_name or "User")
    return f'<a href="tg://user?id={user.id}">{name}</a>'


async def safe_bot(client):
    bot = await client.get_me()
    name = html.escape(bot.first_name)
    return f'<a href="tg://user?id={bot.id}">{name}</a>'


# ================= API SEND HELPERS ================= #

def api_send_photo(chat_id, photo, caption, keyboard=None, effect=None):
    print("\n====== 📸 SENDING PHOTO ======")
    print("chat_id:", chat_id)
    print("caption:", caption)

    payload = {
        "chat_id": chat_id,
        "photo": photo,
        "caption": caption,
        "parse_mode": "HTML",
    }

    if keyboard:
        payload["reply_markup"] = {"inline_keyboard": keyboard}

    if effect:
        payload["message_effect_id"] = effect

    r = requests.post(f"{BOT_API}/sendPhoto", json=payload)
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)
    print("===============================\n")


def api_send_message(chat_id, text, keyboard=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    if keyboard:
        payload["reply_markup"] = {"inline_keyboard": keyboard}

    requests.post(f"{BOT_API}/sendMessage", json=payload)


# ================= START PRIVATE ================= #

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):

    print("\n🔥 /START TRIGGERED")

    await add_served_user(message.from_user.id)

    try:
        await message.react(random.choice(VALID_EMOJII))
    except:
        pass

    random_effect = int(random.choice(EFFECT_IDS))
    args = message.text.split(maxsplit=1)

    mention = safe_mention(message.from_user)
    bot_mention = await safe_bot(client)

    # HELP
    if len(args) > 1 and args[1].startswith("help"):
        keyboard = first_page(_)
        api_send_photo(
            message.chat.id,
            config.START_IMG_URL,
            _["help_1"].format(config.SUPPORT_CHAT),
            keyboard,
            random_effect,
        )
        return

    # SUDO
    if len(args) > 1 and args[1].startswith("sud"):
        await sudoers_list(client=client, message=message, _=_)
        return

    # INFO (🔥 PREMIUM)
    if len(args) > 1 and args[1].startswith("inf"):
        m = await message.reply_text("🔎")

        query = args[1].replace("info_", "", 1)
        query = f"https://www.youtube.com/watch?v={query}"

        results = VideosSearch(query, limit=1)
        result = (await results.next())["result"][0]

        title = result["title"]
        duration = result.get("duration", "Live")
        views = result["viewCount"]["short"]
        published = result["publishedTime"]
        channel = result["channel"]["name"]

        thumb = result["thumbnails"][0]["url"].split("?")[0]
        link = result["link"]

        caption = f"""
<b>🎬 {title}</b>

👤 <b>Channel :</b> {channel}
👁 <b>Views :</b> {views}
⏱ <b>Duration :</b> {duration}
🕒 <b>Uploaded :</b> {published}
"""

        keyboard = [
            [
                {"text": _["S_B_8"], "url": link},
                {"text": _["S_B_9"], "url": config.SUPPORT_CHAT},
            ]
        ]

        await m.delete()

        api_send_photo(
            message.chat.id,
            thumb,
            caption,
            keyboard,
            random_effect,
        )
        return

    # NORMAL START
    panel = private_panel(_)

    caption = _["start_2"].format(mention, bot_mention)

    api_send_photo(
        message.chat.id,
        config.START_IMG_URL,
        caption,
        panel,
        random_effect,
    )

    # ✅ LOG START (NEW)
    try:
        log_text = f"👤 {mention} just started the bot."
        api_send_message(config.LOGGER_ID, log_text)
    except:
        pass

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    try:
        await message.reply_video(
            random.choice(START_VIDS),
            caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
            reply_markup=InlineKeyboardMarkup(out),
        )
    except:
        pass
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except Exception:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_video(
                    random.choice(START_VIDS),
                    caption=_["start_3"].format(
                        message.from_user.mention,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print(ex)
