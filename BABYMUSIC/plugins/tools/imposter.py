from pyrogram import filters
from pyrogram.types import Message
from BABYMUSIC import app
from BABYMUSIC.mongo.pretenderdb import (
    impo_off, impo_on, check_pretender,
    add_userdata, get_userdata, usr_data
)
from BABYMUSIC.utils.admin_filters import admin_filter


@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=69)
async def chk_usr(_, message: Message):
    if message.sender_chat or not await check_pretender(message.chat.id):
        return

    if not await usr_data(message.from_user.id):
        return await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )

    usernamebefore, first_name, lastname_before = await get_userdata(message.from_user.id)

    msg = ""

    if (
        usernamebefore != message.from_user.username
        or first_name != message.from_user.first_name
        or lastname_before != message.from_user.last_name
    ):
        msg += f"""
╭───〔 ⚠️ Pretender Alert 〕───╮
👤 User : {message.from_user.mention}
🆔 ID   : `{message.from_user.id}`
╰──────────────────────╯
"""

    if usernamebefore != message.from_user.username:
        usernamebefore = f"@{usernamebefore}" if usernamebefore else "No Username"
        usernameafter = f"@{message.from_user.username}" if message.from_user.username else "No Username"

        msg += f"""
🔁 Username Changed
• From : {usernamebefore}
• To   : {usernameafter}
"""

        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )

    if first_name != message.from_user.first_name:
        msg += f"""
📝 First Name Updated
• From : {first_name}
• To   : {message.from_user.first_name}
"""

        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )

    if lastname_before != message.from_user.last_name:
        lastname_before = lastname_before or "No Last Name"
        lastname_after = message.from_user.last_name or "No Last Name"

        msg += f"""
📛 Last Name Updated
• From : {lastname_before}
• To   : {lastname_after}
"""

        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )

    if msg:
        await message.reply_text(msg)


# ================== COMMAND ==================

@app.on_message(filters.group & filters.command("imposter") & ~filters.bot & ~filters.via_bot & admin_filter)
async def set_mataa(_, message: Message):

    if len(message.command) == 1:
        return await message.reply(
            "⚙️ Usage:\n`/imposter enable` or `/imposter disable`"
        )

    cmd = message.command[1].lower()

    # ✅ ENABLE (default already ON)
    if cmd == "enable":
        status = await check_pretender(message.chat.id)

        if status:
            return await message.reply("✅ Pretender detection is already enabled.")

        await impo_on(message.chat.id)
        await message.reply(f"🟢 Pretender detection enabled in **{message.chat.title}**")

    # ❌ DISABLE
    elif cmd == "disable":
        status = await check_pretender(message.chat.id)

        if not status:
            return await message.reply("❌ Pretender detection is already disabled.")

        await impo_off(message.chat.id)
        await message.reply(f"🔴 Pretender detection disabled in **{message.chat.title}**")

    else:
        await message.reply("⚠️ Use: `/imposter enable` or `/imposter disable`")
