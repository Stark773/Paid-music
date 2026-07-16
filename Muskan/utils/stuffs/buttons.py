from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums
from Muskan.button_styles import primary_button, success_button, danger_button
import config


class BUTTONS(object):
    ABUTTON = [
        [
            InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url="https://t.me/muskan_music_support"),
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url="https://t.me/muskan_music_official"),
        ],
        [
            InlineKeyboardButton("👑 ᴏᴡɴᴇʀ", user_id=config.OWNER_ID),
            primary_button(text="« ʙᴀᴄᴋ", callback_data="settingsback_helper"),
        ],
    ]

    INFO_BUTTON = [
        [
            primary_button(text="📖 ʜᴇʟᴘ", callback_data="settings_back_helper"),
            primary_button(text="🌐 ʟᴀɴɢ", callback_data="LG"),
        ],
        [
            InlineKeyboardButton("🔒 ᴘʀɪᴠᴀᴄʏ", url="https://docs.google.com/document/d/11Q_ZuvSzkhkgbvVrPxQdqktP2_ioiaqAa7QdsHezfnM/mobilebasic"),
            primary_button(text="« ʙᴀᴄᴋ", callback_data="settingsback_helper"),
        ],
    ]

    INFO_NEW = [
        [
            primary_button(text="« ʙᴀᴄᴋ ᴛᴏ ᴄᴀᴛᴇɢᴏʀɪᴇs", callback_data="settings_back_helper"),
        ],
    ]
