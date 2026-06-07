from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from IQ_Paid import app
from IQ_Paid.button_styles import danger_button, primary_button


def help_pannel(_, START: Union[bool, int] = None):
    first = [danger_button(text=_["CLOSE_BUTTON"], callback_data="close")]
    second = [
        primary_button(
            text=_["BACK_BUTTON"],
            callback_data="settingsback_helper",
        ),
    ]
    mark = second if START else first

    upl = InlineKeyboardMarkup(
        [
            [
                primary_button(
                    text=_["H_B_25"],
                    callback_data="help_callback hb1",
                ),
                primary_button(
                    text=_["H_B_26"],
                    callback_data="help_callback hb2",
                ),
                primary_button(
                    text=_["H_B_28"],
                    callback_data="help_callback hb3",
                ),
            ],
            [
                primary_button(
                    text=_["H_B_27"],
                    callback_data="help_callback hb4",
                ),
                primary_button(
                    text=_["H_B_31"],
                    callback_data="help_callback hb5",
                ),
                primary_button(
                    text=_["H_B_29"],
                    callback_data="help_callback hb6",
                ),
            ],
            [
                primary_button(
                    text=_["H_B_33"],
                    callback_data="help_callback hb7",
                ),
                primary_button(
                    text=_["H_B_30"],
                    callback_data="help_callback hb8",
                ),
                primary_button(
                    text=_["H_B_32"],
                    callback_data="help_callback hb9",
                ),
            ],

            [
                primary_button(
                    text="• ᴀᴄᴛɪᴏɴ •",
                    callback_data="ban_cb",
                ),
                primary_button(
                    text="• ᴍᴏᴅᴇʀᴀᴛɪᴏɴ •",
                    callback_data="mod_cb",
                ),
                primary_button(
                    text="• sᴇᴛᴜᴘ •",
                    callback_data="setup_cb",
                ),
            ],
            [
                primary_button(
                    text="• ᴡᴇʟᴄᴏᴍᴇ •",
                    callback_data="wel_cb",
                ),
                primary_button(
                    text="• ᴠᴄ-ʟᴏɢɢᴇʀ •",
                    callback_data="vc_cb",
                ),
                primary_button(
                    text="• ᴘʀᴏᴍᴏᴛᴇ •",
                    callback_data="ad_cb",
                ),
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
                    text=_["BACK_BUTTON"],
                    callback_data=f"settings_back_helper",
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons
