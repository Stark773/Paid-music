import time
import random
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from py_yt import VideosSearch

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
import config
from Muskan import app
from Muskan.misc import _boot_
from Muskan.plugins.sudo.sudoers import sudoers_list
from Muskan.utils.database import get_served_chats, get_served_users, get_sudoers
from Muskan.utils import bot_sys_stats
from Muskan.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from Muskan.utils.decorators.language import LanguageStart
from Muskan.utils.formatters import get_readable_time
from Muskan.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


MUSKAN_PICS = [
    "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg",
]


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    # ── ᴀɴɪᴍᴀᴛᴇᴅ ᴛʏᴘɪɴɢ ──
    frames = [
        "🎵",
        "🎵 M",
        "🎵 Mu",
        "🎵 Mus",
        "🎵 Musk",
        "🎵 Muska",
        "🎵 Muskan",
        "🎵 Muskan M",
        "🎵 Muskan Mu",
        "🎵 Muskan Mus",
        "🎵 Muskan Musi",
        "🎵 Muskan Music",
        "🎵 Muskan Music ✨",
    ]
    typing_message = await message.reply("<b>🎵</b>")
    for frame in frames:
        try:
            await typing_message.edit_text(f"<b>{frame}</b>")
            await asyncio.sleep(0.07)
        except Exception:
            pass
    await asyncio.sleep(0.5)
    await typing_message.delete()

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)

        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_photo(
                random.choice(MUSKAN_PICS),
                caption=(
                    "**╔══「 📖 Mᴜsᴋᴀɴ ʜᴇʟᴘ ᴄᴇɴᴛᴇʀ 」══╗**\n\n"
                    "🎯 **sᴇʟᴇᴄᴛ ʏᴏᴜʀ ʜᴇʟᴘ ᴄᴀᴛᴇɢᴏʀʏ** ʙᴇʟᴏᴡ\n\n"
                    f"💬 ᴀsᴋ ᴅᴏᴜʙᴛs ᴀᴛ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ]({config.SUPPORT_CHAT})\n\n"
                    "**╚══「 🎵 Mᴜsᴋᴀɴ Mᴜsɪᴄ 」══╝**"
                ),
                reply_markup=keyboard,
                has_spoiler=False,
            )

        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} checked <b>sudolist</b>.\n\n<b>User ID :</b> <code>{message.from_user.id}</code>\n<b>Username :</b> @{message.from_user.username}",
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
                await m.delete()
                img = await message.reply_photo(thumbnail)
                await img.reply_text(
                    f"<b>🎵 {title}</b>\n\n"
                    f"<b>⏱ Duration :</b> {duration}\n"
                    f"<b>👁 Views :</b> {views}\n"
                    f"<b>📺 Channel :</b> <a href='{channellink}'>{channel}</a>\n"
                    f"<b>🔗 Link :</b> {link}",
                    disable_web_page_preview=True,
                )
            return

    out = start_panel(_)
    await message.reply_photo(
        photo=random.choice(MUSKAN_PICS),
        caption=(
            f"**✦ ʜᴇʟʟᴏ {message.from_user.mention} 🥀**\n\n"
            f"**╔══「 🎵 {app.mention} 」══╗**\n\n"
            "➻ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ\n"
            "    ʙᴜɪʟᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs & ᴄʜᴀɴɴᴇʟs\n\n"
            "✦ ʜɪɢʜ ǫᴜᴀʟɪᴛʏ  •  ɴᴏ ʟᴀɢ  •  24/7\n\n"
            "📖 ᴛᴀᴘ **ʜᴇʟᴘ** ᴛᴏ sᴇᴇ ᴀʟʟ ᴄᴀᴛᴇɢᴏʀɪᴇs\n\n"
            f"**╚══「 [˹Mᴜsᴋᴀɴ˼]({config.SUPPORT_CHAT}) 」══╝**"
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_group(client, message: Message, _):
    out = start_panel(_)
    await message.reply_photo(
        photo=random.choice(MUSKAN_PICS),
        caption=(
            f"**✦ ʜᴇʏ {message.from_user.mention} 🎶**\n\n"
            f"**{app.mention}** ɪs ɴᴏᴡ ʀᴇᴀᴅʏ ɪɴ\n"
            f"**{message.chat.title}** ✨\n\n"
            "▶️ ᴜsᴇ /play ᴛᴏ sᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ!\n"
            "📖 ᴛᴀᴘ **ʜᴇʟᴘ** ғᴏʀ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs."
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
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
                    random.choice(MUSKAN_PICS),
                    caption=(
                        f"**✦ ʜᴇʏ {message.from_user.mention} 🎶**\n\n"
                        f"**{app.mention}** ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ\n"
                        f"**{message.chat.title}** ✨\n\n"
                        "▶️ ᴜsᴇ /play ᴛᴏ sᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ!\n"
                        "📖 ᴛᴀᴘ **ʜᴇʟᴘ** ғᴏʀ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs."
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            pass

# ©️ 2025-26 Muskan Music Bot
