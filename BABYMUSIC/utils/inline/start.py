import config
from BABYMUSIC import app
from pyrogram.types import WebAppInfo
from BABYMUSIC.button_styles import primary_button, success_button, danger_button


def start_panel(_):
    buttons = [
        [
            primary_button(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            success_button(text=_["S_B_2"], url=config.SUPPORT_CHANNEL),
        ],
    ]
    return buttons



def private_panel(_):
    return [

        # 1️⃣ SINGLE BUTTON
        [
            {
                "text": _["S_B_3"],
                "url": f"https://t.me/{app.username}?startgroup=true",
                "style": "primary"
            }
        ],

        # 2️⃣ TWO BUTTONS
        [
            {
                "text": _["S_B_4"],
                "callback_data": "open_help",
                "style": "danger"
            },
            {
                "text": "BabiesＩＱ™",
                "url": "https://t.me/BabiesIQ",
                "style": "success"
            },
        ],

        # 3️⃣ TWO BUTTONS
        [
            {
                "text": ". ♬ ݁˖",
                "url": "https://t.me/YoutubeVcBoT",
                "style": "success"
            },
            {
                "text": "𖠋",
                "url": "https://t.me/Radhikacallbot",
                "style": "danger"
            },
        ],

        # 5️⃣ LAST WEB APP BUTTON
        [
            {
                "text": "| ᴶᴼᴵᴺ ᵀᴼᴰᴬᵞ BabiesＩＱ™ |",
                "web_app": {"url": "https://babyapi.pro"},
                "style": "primary"
            }
        ],
    ]


def iprivate_panel(_):
    buttons = [
        [
            primary_button(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            danger_button(text=_["S_B_4"], callback_data="open_help"),
            success_button(text=_["S_B_5"], url="https://t.me/BabiesIQ"),
        ],
        [
            success_button(text=_["S_B_6"], url="https://t.me/YoutubeVcBoT"),
            danger_button(text=_["S_B_7"], url="https://t.me/Radhikacallbot"),
        ],
        [
            primary_button(
                text=_["S_B_8"],
                web_app=WebAppInfo(url="https://babyapi.pro")
            ),
        ],
    ]
    return buttons
