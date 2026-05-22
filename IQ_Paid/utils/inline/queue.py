from typing import Union
from IQ_Paid import app
from IQ_Paid.utils.formatters import time_to_seconds
from IQ_Paid.button_styles import danger_button, primary_button
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def queue_markup(
    _,
    DURATION,
    CPLAY,
    videoid,
    played: Union[bool, int] = None,
    dur: Union[bool, int] = None,
):
    not_dur = [
        [
            primary_button(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
            ),
            danger_button(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
            ),
        ]
    ]
    dur = [
        [
            primary_button(
                text=_["QU_B_2"].format(played, dur),
                callback_data="GetTimer",
            )
        ],
        [
            primary_button(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
            ),
            danger_button(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
            ),
        ],
    ]
    upl = InlineKeyboardMarkup(not_dur if DURATION == "Unknown" else dur)
    return upl


def queue_back_markup(_, CPLAY):
    upl = InlineKeyboardMarkup(
        [
            [
                primary_button(
                    text=_["BACK_BUTTON"],
                    callback_data=f"queue_back_timer {CPLAY}",
                ),
                danger_button(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ]
        ]
    )
    return upl


def aq_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="ᴊᴏɪɴ ɴᴏᴡ",
                url=f"https://t.me/+8WjqAqBihwkyNzk9"
            ),
            InlineKeyboardButton(
                text="ɢʀᴏᴜᴘ ᴄʜᴧᴛ",
                url="https://t.me/+8WjqAqBihwkyNzk9"
            ),
        ],
        [
            danger_button(
                text="ᴄʟᴏsᴇ",
                callback_data="close"
            )
        ],
    ]
    return buttons
