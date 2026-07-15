import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from Muskan import LOGGER, app, userbot
from Muskan.core.call import Muskan as MusicCall
from Muskan.misc import sudo
from Muskan.plugins import ALL_MODULES
from Muskan.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3,
                config.STRING4, config.STRING5]):
        LOGGER(__name__).error(
            "STRING SESSION NOT FILLED! Please fill at least one Pyrogram session string."
        )
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("Muskan.plugins" + all_module)
    LOGGER("Muskan.plugins").info("ALL PLUGINS LOADED SUCCESSFULLY ✅")
    await userbot.start()
    await MusicCall.start()
    try:
        await MusicCall.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("Muskan").error(
            "Please START your LOG GROUP/CHANNEL Voice Chat... Music Bot stopped."
        )
        exit()
    except Exception:
        pass
    await MusicCall.decorators()
    LOGGER("Muskan").info(
        "╔══════════════════════╗\n"
        "   🎵  MUSKAN MUSIC BOT  🎵\n"
        "╚══════════════════════╝"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("Muskan").info("Muskan Music Bot stopped.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
