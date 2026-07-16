from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Muskan import app
from Muskan.button_styles import danger_button, primary_button, success_button


def help_pannel(_, START: Union[bool, int] = None):
    close_row = [danger_button(text="✖ ᴄʟᴏsᴇ", callback_data="close")]
    back_row = [primary_button(text="« ʙᴀᴄᴋ", callback_data="settingsback_helper")]
    mark = back_row if START else close_row

    upl = InlineKeyboardMarkup(
        [
            [
                primary_button(text="🎛️ ᴀᴅᴍɪɴ", callback_data="help_callback hb1"),
                primary_button(text="🔐 ᴀᴜᴛʜ", callback_data="help_callback hb2"),
            ],
            [
                primary_button(text="📢 ʙʀᴏᴀᴅᴄᴀsᴛ", callback_data="help_callback hb3"),
                primary_button(text="🚫 ʙʟᴀᴄᴋʟɪsᴛ", callback_data="help_callback hb4"),
            ],
            [
                primary_button(text="🎶 ᴘʟᴀʏ", callback_data="help_callback hb5"),
                primary_button(text="🎛 ɢ-ʙᴀɴ", callback_data="help_callback hb6"),
            ],
            [
                primary_button(text="📥 ᴅᴏᴡɴʟᴏᴀᴅ", callback_data="help_callback hb7"),
                primary_button(text="⚙️ sᴇᴛᴜᴘ", callback_data="help_callback hb8"),
            ],
            [
                primary_button(text="📌 ᴠᴄ ʟᴏɢɢᴇʀ", callback_data="help_callback hb9"),
                primary_button(text="🛡️ ᴍᴏᴅᴇʀᴀᴛɪᴏɴ", callback_data="help_callback hb10"),
            ],
            [
                primary_button(text="📣 ᴘʀᴏᴍᴏᴛᴇ", callback_data="help_callback hb11"),
                primary_button(text="🏠 ɢʀᴘ ᴛᴏᴏʟs", callback_data="help_callback hb12"),
            ],
            [
                primary_button(text="👋 ᴡᴇʟᴄᴏᴍᴇ", callback_data="help_callback hb13"),
                primary_button(text="ℹ️ ᴀʙᴏᴜᴛ", callback_data="help_callback hb14"),
            ],
            [
                success_button(text="🔗 sᴜᴘᴘᴏʀᴛ", callback_data="help_callback hb15"),
            ],
            mark,
        ]
    )
    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                primary_button(
                    text="« ʙᴀᴄᴋ ᴛᴏ ᴄᴀᴛᴇɢᴏʀɪᴇs",
                    callback_data="settings_back_helper",
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="📖 ɢᴇᴛ ʜᴇʟᴘ ɪɴ ᴘᴍ",
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons
