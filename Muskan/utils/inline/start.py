from pyrogram.types import InlineKeyboardButton

from Muskan.button_styles import primary_button, success_button
import config
from Muskan import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ ᴀᴅᴅ Mᴜsᴋᴀɴ",
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
            InlineKeyboardButton(
                text="💬 sᴜᴘᴘᴏʀᴛ",
                url=config.SUPPORT_CHAT,
            ),
        ],
        [
            primary_button(text="📖 ʜᴇʟᴘ", callback_data="settings_back_helper"),
            primary_button(text="ℹ️ ᴀʙᴏᴜᴛ", callback_data="abot_cb"),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            primary_button(text="🔗 sᴜᴘᴘᴏʀᴛ", callback_data="sbot_cb"),
            primary_button(text="ℹ️ ᴀʙᴏᴜᴛ", callback_data="abot_cb"),
        ],
        [
            success_button(text="📖 ʜᴇʟᴘ ᴍᴇɴᴜ", callback_data="settings_back_helper"),
        ],
    ]
    return buttons
