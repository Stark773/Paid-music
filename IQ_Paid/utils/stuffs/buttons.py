from pyrogram.types import InlineKeyboardButton
from IQ_Paid.button_styles import primary_button, success_button
import config


class BUTTONS(object):

    ABUTTON = [
        [
            success_button(text="📣", url="https://t.me/+8WjqAqBihwkyNzk9"),
            InlineKeyboardButton(text="ᴏᴡɴᴇʀ", user_id=config.OWNER_ID),
            success_button(text="📞", url="https://t.me/+8WjqAqBihwkyNzk9")
        ],
        [
            primary_button(
                text="• ʙᴧᴄᴋ •",
                callback_data="settingsback_helper"
            )
        ]
    ]

    INFO_BUTTON = [
        [
            InlineKeyboardButton(
                text="ᴘʀɪᴠᴧᴄʏ",
                url="https://docs.google.com/document/d/11Q_ZuvSzkhkgbvVrPxQdqktP2_ioiaqAa7QdsHezfnM/mobilebasic"
            ),
            primary_button(
                text="• ʙᴧᴄᴋ •",
                callback_data="settingsback_helper"
            ),
        ]
    ]

    INFO_NEW = [
        [
            primary_button(
                text="• ʙᴧᴄᴋ •",
                callback_data="settings_back_helper"
            )
        ]
    ]
