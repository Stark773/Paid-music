from pyrogram.types import InlineKeyboardButton

from IQ_Paid.button_styles import primary_button, success_button, danger_button
import config
from IQ_Paid import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            primary_button(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            danger_button(text=_["S_B_9"], callback_data="sbot_cb"),
            danger_button(text=_["S_B_13"], callback_data="abot_cb"),
        ],
        [
            success_button(text=_["S_B_4"], callback_data="settings_back_helper"),
        ],
    ]
    return buttons
