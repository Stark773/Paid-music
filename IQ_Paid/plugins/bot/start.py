import time
import random
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message
from py_yt import VideosSearch

import config
from IQ_Paid import app
from IQ_Paid.misc import _boot_
from IQ_Paid.plugins.sudo.sudoers import sudoers_list
from IQ_Paid.utils.database import get_served_chats, get_served_users, get_sudoers
from IQ_Paid.utils import bot_sys_stats
from IQ_Paid.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from IQ_Paid.utils.decorators.language import LanguageStart
from IQ_Paid.utils.formatters import get_readable_time
from IQ_Paid.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS, START_IMG_URL
from strings import get_string



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Premium symbol-only loading animation
#  left  → braille spinner  ⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏
#  right → ▱ fills to ▰ then sweeps back, ends ◉ ▰▰▰▰▰▰▰▰▰▰
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_SPIN  = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
_EMPTY = "▱"
_FULL  = "▰"
_BAR_W = 10


def _make_bar(filled: int) -> str:
    return _FULL * filled + _EMPTY * (_BAR_W - filled)


_FRAMES: list[str] = []
for _i in range(_BAR_W + 1):
    _FRAMES.append(f"{_SPIN[_i % len(_SPIN)]}  {_make_bar(_i)}")
for _i in range(_BAR_W, -1, -1):
    _FRAMES.append(f"{_SPIN[(_BAR_W + (_BAR_W - _i)) % len(_SPIN)]}  {_make_bar(_i)}")
_FRAMES.append(f"◉  {'▰' * _BAR_W}")


async def _show_loading(message: Message) -> None:
    loader = await message.reply(_FRAMES[0])
    for frame in _FRAMES[1:]:
        try:
            await loader.edit_text(frame)
        except Exception:
            pass
        await asyncio.sleep(0.13)
    await asyncio.sleep(0.25)
    try:
        await loader.delete()
    except Exception:
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /start — Private
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    await _show_loading(message)

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name[0:3] == "del":
            return await del_plist_msg(client=client, message=message, _=_)

        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_photo(
                START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
                has_spoiler=True,
            )

        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                        f"<b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"
                        f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                        f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
                    ),
                )
            return

        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
                has_spoiler=True,
            )
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                        f"<b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n"
                        f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                        f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
                    ),
                )
            return

    else:
        out = private_panel(_)
        await message.reply_photo(
            START_IMG_URL,
            caption=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(out),
            has_spoiler=True,
        )
        if await is_on_off(2):
            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                    f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                    f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
                ),
            )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /start — Group
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
        has_spoiler=True,
    )
    return await add_served_chat(message.chat.id)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  New chat member handler
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
                await message.reply_photo(
                    START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.mention,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                    has_spoiler=True,
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)


# ===========================================================
# ©️ 2025-26 All Rights Reserved by Team IQ_Paid
# ===========================================================
