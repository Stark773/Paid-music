from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class Muskan(Client):
    def __init__(self):
        LOGGER(__name__).info("» Starting Muskan Music Bot...")
        super().__init__(
            name="Muskan",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<u><b>🎵 {self.mention} Started :</b></u>\n\n"
                    f"ID : <code>{self.id}</code>\n"
                    f"Name : {self.name}\n"
                    f"Username : @{self.username}\n\n"
                    f"<b>Muskan Music Bot is Online ✅</b>"
                ),
            )
        except Exception:
            LOGGER(__name__).error(
                "» Bot failed to access log group/channel. Make sure bot is added and is admin."
            )
        try:
            a = await self.get_chat_member(config.LOGGER_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("» Please promote bot as admin in your log group/channel.")
        except Exception:
            pass
        LOGGER(__name__).info(f"✦ Muskan Music Bot started as {self.name}")

    async def stop(self):
        await super().stop()
