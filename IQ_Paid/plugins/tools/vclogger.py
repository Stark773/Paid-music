from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, Message
from pytgcalls import filters as fl
from pytgcalls.types import GroupCallParticipant

import config
from IQ_Paid import app
from IQ_Paid.core.call import Istu
from IQ_Paid.misc import SUDOERS
from IQ_Paid.utils.database import (
    get_chat,
    is_vc_logger,
    set_vc_logger,
)
from IQ_Paid.button_styles import danger_button, primary_button, success_button


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  VC Participant — Joined Handler
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
async def _on_participant_joined(client, update: GroupCallParticipant):
    try:
        chat_id = update.chat_id
        if not await is_vc_logger(chat_id):
            return
        if not config.LOGGER_ID:
            return
        user_id = update.user_id
        try:
            user = await app.get_users(user_id)
            mention = user.mention
        except Exception:
            mention = f"[User](tg://user?id={user_id})"
        try:
            chat = await app.get_chat(chat_id)
            chat_title = chat.title or str(chat_id)
        except Exception:
            chat_title = str(chat_id)
        text = (
            "**#ᴠᴄ_ʟᴏɢ | ᴊᴏɪɴᴇᴅ ✅**\n\n"
            f"**• ᴜsᴇʀ:** {mention}\n"
            f"**• ᴜsᴇʀ ɪᴅ:** `{user_id}`\n"
            f"**• ᴄʜᴀᴛ:** {chat_title}\n"
            f"**• ᴄʜᴀᴛ ɪᴅ:** `{chat_id}`\n"
            f"**• ᴀᴄᴛɪᴏɴ:** ᴊᴏɪɴᴇᴅ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"
        )
        try:
            await app.send_message(
                config.LOGGER_ID,
                text,
                disable_web_page_preview=True,
            )
        except Exception:
            pass
    except Exception:
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  VC Participant — Left Handler
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
async def _on_participant_left(client, update: GroupCallParticipant):
    try:
        chat_id = update.chat_id
        if not await is_vc_logger(chat_id):
            return
        if not config.LOGGER_ID:
            return
        user_id = update.user_id
        try:
            user = await app.get_users(user_id)
            mention = user.mention
        except Exception:
            mention = f"[User](tg://user?id={user_id})"
        try:
            chat = await app.get_chat(chat_id)
            chat_title = chat.title or str(chat_id)
        except Exception:
            chat_title = str(chat_id)
        text = (
            "**#ᴠᴄ_ʟᴏɢ | ʟᴇꜰᴛ ❌**\n\n"
            f"**• ᴜsᴇʀ:** {mention}\n"
            f"**• ᴜsᴇʀ ɪᴅ:** `{user_id}`\n"
            f"**• ᴄʜᴀᴛ:** {chat_title}\n"
            f"**• ᴄʜᴀᴛ ɪᴅ:** `{chat_id}`\n"
            f"**• ᴀᴄᴛɪᴏɴ:** ʟᴇꜰᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"
        )
        try:
            await app.send_message(
                config.LOGGER_ID,
                text,
                disable_web_page_preview=True,
            )
        except Exception:
            pass
    except Exception:
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Register callbacks on ALL non-None pytgcalls clients
#  Fixes: AttributeError: 'NoneType' object has no attribute 'on_update'
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def _register_vc_callbacks():
    _clients = [
        Istu.one,
        Istu.two,
        Istu.three,
        Istu.four,
        Istu.five,
    ]
    for _c in _clients:
        if _c is None:
            continue
        _c.on_update(
            fl.call_participant(GroupCallParticipant.Action.JOINED)
        )(_on_participant_joined)
        _c.on_update(
            fl.call_participant(GroupCallParticipant.Action.LEFT)
        )(_on_participant_left)


_register_vc_callbacks()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /vclog command — enable / disable per group
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_USAGE = (
    "**ᴠᴄ ʟᴏɢɢᴇʀ ᴜsᴀɢᴇ:**\n\n"
    "`/vclog enable` — ᴇɴᴀʙʟᴇ ᴠᴄ ʟᴏɢɢɪɴɢ ꜰᴏʀ ᴛʜɪs ɢʀᴏᴜᴘ\n"
    "`/vclog disable` — ᴅɪsᴀʙʟᴇ ᴠᴄ ʟᴏɢɢɪɴɢ ꜰᴏʀ ᴛʜɪs ɢʀᴏᴜᴘ\n"
    "`/vclog status` — ᴄʜᴇᴄᴋ ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs"
)


@app.on_message(filters.command(["vclog", "vclogger"]) & filters.group)
async def vclog_command(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            _USAGE,
            reply_markup=InlineKeyboardMarkup(
                [[danger_button(text="⌯ ᴄʟᴏsᴇ ⌯", callback_data="close")]]
            ),
        )

    chat_id = message.chat.id
    action = message.command[1].lower()

    if message.from_user.id not in SUDOERS:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status not in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        ):
            return await message.reply_text(
                "**ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.**",
                reply_markup=InlineKeyboardMarkup(
                    [[danger_button(text="⌯ ᴄʟᴏsᴇ ⌯", callback_data="close")]]
                ),
            )

    if action == "enable":
        await set_vc_logger(chat_id, True)
        await message.reply_text(
            "**ᴠᴄ ʟᴏɢɢᴇʀ ᴇɴᴀʙʟᴇᴅ ✅**\n\n"
            "ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ ᴊᴏɪɴ/ʟᴇᴀᴠᴇ ᴇᴠᴇɴᴛs ᴡɪʟʟ ɴᴏᴡ ʙᴇ ʟᴏɢɢᴇᴅ.",
            reply_markup=InlineKeyboardMarkup(
                [[success_button(text="✔ ᴇɴᴀʙʟᴇᴅ", callback_data="close")]]
            ),
        )

    elif action == "disable":
        await set_vc_logger(chat_id, False)
        await message.reply_text(
            "**ᴠᴄ ʟᴏɢɢᴇʀ ᴅɪsᴀʙʟᴇᴅ ❌**\n\n"
            "ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ ᴇᴠᴇɴᴛs ᴡɪʟʟ ɴᴏ ʟᴏɴɢᴇʀ ʙᴇ ʟᴏɢɢᴇᴅ.",
            reply_markup=InlineKeyboardMarkup(
                [[danger_button(text="✖ ᴅɪsᴀʙʟᴇᴅ", callback_data="close")]]
            ),
        )

    elif action == "status":
        enabled = await is_vc_logger(chat_id)
        logger_set = bool(config.LOGGER_ID)
        status_text = "ᴇɴᴀʙʟᴇᴅ ✅" if enabled else "ᴅɪsᴀʙʟᴇᴅ ❌"
        logger_info = f"`{config.LOGGER_ID}`" if logger_set else "ɴᴏᴛ sᴇᴛ ⚠️"
        await message.reply_text(
            f"**ᴠᴄ ʟᴏɢɢᴇʀ sᴛᴀᴛᴜs**\n\n"
            f"**• sᴛᴀᴛᴜs:** {status_text}\n"
            f"**• ʟᴏɢɢᴇʀ ɪᴅ:** {logger_info}",
            reply_markup=InlineKeyboardMarkup(
                [[danger_button(text="⌯ ᴄʟᴏsᴇ ⌯", callback_data="close")]]
            ),
        )

    else:
        await message.reply_text(
            _USAGE,
            reply_markup=InlineKeyboardMarkup(
                [[danger_button(text="⌯ ᴄʟᴏsᴇ ⌯", callback_data="close")]]
            ),
        )
