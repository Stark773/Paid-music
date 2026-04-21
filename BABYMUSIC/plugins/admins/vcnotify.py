from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from BABYMUSIC import app
from BABYMUSIC.core.call import JARVIS
from BABYMUSIC.utils.database import get_cmode, get_vcnotify, set_vcnotify
from BABYMUSIC.utils.decorators.admins import AdminActual
from BABYMUSIC.utils.inline import close_markup


# ---------------- AUTO HANDLER ---------------- #

@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=68)
async def auto_vc_notify(_, message: Message):
    try:
        chat_id = message.chat.id

        # 🔹 DB check (auto ON bhi yahi karega)
        status = await get_vcnotify(chat_id)

        # ❌ Manual OFF respect
        if not status:
            return

        # 🔹 Already running → skip
        if chat_id in JARVIS.vc_notifier:
            return

        # 🔹 Start notifier
        await JARVIS.maybe_start_vc_join_notifier(chat_id, chat_id)

        # 🔹 Linked chat support
        linked_chat = await get_cmode(chat_id)
        if linked_chat:
            if linked_chat not in JARVIS.vc_notifier:
                await JARVIS.maybe_start_vc_join_notifier(linked_chat, chat_id)

    except Exception:
        pass  # 🔇 silent

# ---------------- COMMAND ---------------- #

@app.on_message(filters.command(["vcnotify"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def vcnotify_control(_, message: Message, strings):
    chat_id = message.chat.id

    # 🔹 Status check
    if len(message.command) == 1:
        status = "enabled" if await get_vcnotify(chat_id) else "disabled"
        return await message.reply_text(
            f"» VC notify is <code>{status}</code>.",
            reply_markup=close_markup(strings),
        )

    state = message.text.split(None, 1)[1].lower()
    linked_chat = await get_cmode(chat_id)

    # ✅ ENABLE
    if state in {"on", "enable", "enabled", "yes"}:
        await set_vcnotify(chat_id, True)

        await JARVIS.maybe_start_vc_join_notifier(chat_id, chat_id)

        if linked_chat:
            await JARVIS.maybe_start_vc_join_notifier(linked_chat, chat_id)

        return await message.reply_text(
            f"» VC notify <code>enabled</code> by {message.from_user.mention}.",
            reply_markup=close_markup(strings),
        )

    # ❌ DISABLE
    elif state in {"off", "disable", "disabled", "no"}:
        await set_vcnotify(chat_id, False)

        await JARVIS.stop_vc_join_notifier(chat_id)

        if linked_chat:
            await JARVIS.stop_vc_join_notifier(linked_chat)

        return await message.reply_text(
            f"» VC notify <code>disabled</code> by {message.from_user.mention}.",
            reply_markup=close_markup(strings),
        )

    return await message.reply_text(
        "<b>Usage:</b>\n/vcnotify on | off",
        reply_markup=close_markup(strings),
    )
