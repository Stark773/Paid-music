from datetime import datetime
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from pyrogram.enums import ParseMode
from config import OWNER_ID
from BABYMUSIC import app


LOG_GROUP_ID = -1002667870369


def extract_bug_content(msg: Message) -> str | None:
    if msg.reply_to_message:
        return msg.reply_to_message.text or "ᴍᴇᴅɪᴀ ʀᴇᴘᴏʀᴛ"
    return msg.text.split(None, 1)[1] if msg.text and " " in msg.text else None


def escape_md(text: str) -> str:
    return text.replace('[', '\\[').replace(']', '\\]').replace('`', '\\`')


# ================= REPORT COMMAND ================= #

@app.on_message(filters.command("report"))
async def report_bug(_, msg: Message):

    bug_description = extract_bug_content(msg)

    # 👉 PREMIUM GUIDE
    if not bug_description:
        return await msg.reply_text(
            "**╭───〔 📢 ʀᴇᴘᴏʀᴛ ɢᴜɪᴅᴇ 〕───╮**\n"
            "**│**\n"
            "**│ ✦ ʜᴏᴡ ᴛᴏ ʀᴇᴘᴏʀᴛ ?**\n"
            "**│ ➤ ᴜsᴇ /report ᴡɪᴛʜ ᴍᴇssᴀɢᴇ\n"
            "**│ ➤ ᴏʀ ʀᴇᴘʟʏ + /report\n"
            "**│**\n"
            "**│ ✦ ᴡʜᴀᴛ ᴛᴏ ᴡʀɪᴛᴇ ?**\n"
            "**│ ➤ ᴄʟᴇᴀʀ ɪssᴜᴇ / ʙᴜɢ\n"
            "**│ ➤ ᴇʀʀᴏʀ / ʟᴀɢ / ᴘʀᴏʙʟᴇᴍ\n"
            "**│ ➤ ғᴇᴀᴛᴜʀᴇ sᴜɢɢᴇsᴛɪᴏɴ\n"
            "**│**\n"
            "**│ ✦ ᴇxᴀᴍᴘʟᴇ :**\n"
            "**│ ➤ `/report song not playing`\n"
            "**│ ➤ `/report add playlist`\n"
            "**│**\n"
            "**│ ✦ ɴᴏᴛᴇ :**\n"
            "**│ ➤ ᴅᴇᴠ ᴡɪʟʟ ʀᴇᴠɪᴇᴡ ⚡\n"
            "**│ ➤ ʏᴏᴜ ɢᴇᴛ ɴᴏᴛɪғɪᴇᴅ ✅\n"
            "**│**\n"
            "**╰───────────────╯**"
        )

    user_id = msg.from_user.id
    user_name = escape_md(msg.from_user.first_name)
    mention = f"[{user_name}](tg://user?id={user_id})"

    chat_reference = (
        f"@{msg.chat.username}"
        if msg.chat.username
        else f"`{msg.chat.id}`"
    )

    current_date = datetime.utcnow().strftime("%d-%m-%Y")

    # 👉 REPORT FORMAT
    bug_report = (
        f"**╭───〔 🐞 ʀᴇᴘᴏʀᴛ 〕───╮**\n"
        f"**│ 👤 ᴜsᴇʀ :** {mention}\n"
        f"**│ 🆔 ɪᴅ :** `{user_id}`\n"
        f"**│ 💬 ᴄʜᴀᴛ :** {chat_reference}\n"
        f"**│ 📅 ᴅᴀᴛᴇ :** `{current_date}`\n"
        f"**│**\n"
        f"**│ ✦ ᴍᴇssᴀɢᴇ :**\n"
        f"**│ `{escape_md(bug_description)}`\n"
        f"**│**\n"
        f"**│ 🔄 sᴛᴀᴛᴜs :** `pending`\n"
        f"**╰───────────────╯**"
    )

    # 👉 USER CONFIRM
    await msg.reply_text(
        "**╭───〔 ✅ ʀᴇᴘᴏʀᴛ sᴇɴᴛ 〕───╮**\n"
        "**│ ʏᴏᴜʀ ɪssᴜᴇ ʀᴇᴀᴄʜᴇᴅ ᴅᴇᴠ ⚡\n"
        "**│ ᴡᴀɪᴛ ғᴏʀ ʀᴇsᴏʟᴠᴇ...\n"
        "**╰───────────────╯**"
    )

    # 👉 BUTTONS (DEV PANEL)
    buttons = [
        [
            InlineKeyboardButton(
                "✅ ʀᴇsᴏʟᴠᴇ",
                callback_data=f"resolve|{user_id}"
            ),
            InlineKeyboardButton(
                "✖ ᴄʟᴏsᴇ",
                callback_data="close_report"
            )
        ]
    ]

    await app.send_message(
        LOG_GROUP_ID,
        bug_report,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ================= RESOLVE ================= #

@app.on_callback_query(filters.regex("^resolve"))
async def resolve_report(_, query: CallbackQuery):

    if query.from_user.id != OWNER_ID:
        return await query.answer("❌ ᴏɴʟʏ ᴅᴇᴠ", show_alert=True)

    user_id = int(query.data.split("|")[1])

    # 👉 UPDATE STATUS
    text = query.message.text.replace("pending", "resolved ✅")

    await query.message.edit_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✖ ᴄʟᴏsᴇ", callback_data="close_report")]]
        )
    )

    # 👉 NOTIFY USER
    try:
        await app.send_message(
            user_id,
            "**╭───〔 ✅ ʀᴇsᴏʟᴠᴇᴅ 〕───╮**\n"
            "**│ ʏᴏᴜʀ ʀᴇᴘᴏʀᴛ ғɪxᴇᴅ 🎉\n"
            "**│ ᴛʜᴀɴᴋ ʏᴏᴜ ❤️\n"
            "**╰───────────────╯**"
        )
    except:
        await query.answer("⚠️ ᴜsᴇʀ ɴᴏᴛ sᴛᴀʀᴛ ʙᴏᴛ", show_alert=True)


# ================= CLOSE ================= #

@app.on_callback_query(filters.regex("close_report"))
async def close_report(_, query: CallbackQuery):
    try:
        await query.message.delete()
    except:
        pass
