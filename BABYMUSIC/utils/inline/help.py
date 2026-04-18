from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from BABYMUSIC import app
from BABYMUSIC.button_styles import danger_button, primary_button


TOTAL_SECTIONS = 24
BUTTON_LABEL_OVERRIDES = {
    25: "Dᴏᴡɴʟᴏᴀᴅ",
}


def generate_help_buttons(_, start: int, end: int, current_page: int):
    buttons = []
    per_row = 2
    for idx, section in enumerate(range(start, end + 1)):
        if idx % per_row == 0:
            buttons.append([])
        buttons[-1].append(
            InlineKeyboardButton(
                text=BUTTON_LABEL_OVERRIDES.get(section, _[f"H_B_{section}"]),
                callback_data=f"help_callback hb{section}_p{current_page}",
            )
        )
    return buttons


def first_page(_):
    buttons = generate_help_buttons(_, 1, 12, current_page=1)
    buttons.append(
        [
            primary_button(text="↺", callback_data="help_next_2"),
            primary_button(text="↻", callback_data="help_next_2"),
        ]
    )
    buttons.append(
        [
            primary_button(text="Ė x ɪ ᴛ ⌂", callback_data="back_to_main")
        ]
    )
    return InlineKeyboardMarkup(buttons)


def second_page(_):
    buttons = generate_help_buttons(_, 13, TOTAL_SECTIONS, current_page=2)
    buttons.append(
        [
            primary_button(text="↺", callback_data="help_prev_1"),
            primary_button(text="↻", callback_data="help_prev_1"),
        ]
    )
    buttons.append(
        [
            primary_button(text="Ė x ɪ ᴛ ⌂", callback_data="back_to_main")
        ]
    )
    return InlineKeyboardMarkup(buttons)

def action_sub_menu(_, current_page: int):
    return InlineKeyboardMarkup(
        [
            [
                primary_button(text=_["H_B_S_1"], callback_data="action_prom_1"),
                primary_button(text=_["H_B_S_2"], callback_data="action_pun_1"),
            ],
            [
                primary_button(
                    text=_["BACK_BUTTON"],
                    callback_data=f"help_back_{current_page}",
                )
            ],
        ]
    )


def help_back_markup(_, current_page: int):
    return InlineKeyboardMarkup(
        [
            [
                primary_button(
                    text=_["BACK_BUTTON"],
                    callback_data=f"help_back_{current_page}",
                ),
                danger_button(text=_["CLOSE_BUTTON"], callback_data="close"),
            ]
        ]
    )


def private_help_panel(_):
    return [
        [
            primary_button(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?start=help",
            )
        ]
    ]
