from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from BABYMUSIC.misc import db
from BABYMUSIC.button_styles import danger_button, primary_button, success_button


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
            InlineKeyboardButton(
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
    queue_text = "No song in queue"

    if chat_id in db and len(db[chat_id]) > 1:
        last_index = len(db[chat_id]) - 1
        track = db[chat_id][last_index]
        title = track["title"]
        queue_text = f"Next ➜ {last_index}. {title[:15]}"

    buttons = [
        [
            success_button(
                text=queue_text,
                callback_data=f"ADMIN Skip|{chat_id}"
            )
        ]
    ]
    return buttons
