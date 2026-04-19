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

    user_id = message.from_user.id

    # 👉 full user (bio ke liye)
    full_user = await app.get_users(user_id)
    bio = full_user.bio or "No Bio"

    # 👉 first time save (bio ke sath)
    if not await usr_data(user_id):
        return await add_userdata(
            user_id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            bio
        )

    usernamebefore, first_name, lastname_before, bio_before = await get_userdata(user_id)

    changes = []

    # username
    if usernamebefore != message.from_user.username:
        before = f"@{usernamebefore}" if usernamebefore else "No Username"
        after = f"@{message.from_user.username}" if message.from_user.username else "No Username"

        changes.append(f"🔁 **Username**\n» {before} ➜ {after}")

    # first name
    if first_name != message.from_user.first_name:
        changes.append(f"📝 **First Name**\n» {first_name} ➜ {message.from_user.first_name}")

    # last name
    if lastname_before != message.from_user.last_name:
        before = lastname_before or "No Last Name"
        after = message.from_user.last_name or "No Last Name"

        changes.append(f"📛 **Last Name**\n» {before} ➜ {after}")

    # bio
    if bio_before != bio:
        before = bio_before or "No Bio"
        after = bio or "No Bio"

        changes.append(f"🧬 **Bio Changed**\n» {before}\n➜ {after}")

    # 👉 agar koi bhi change hua
    if changes:
        msg = f"""
╭━━━〔 🚨 𝗣𝗥𝗘𝗧𝗘𝗡𝗗𝗘𝗥 𝗔𝗟𝗘𝗥𝗧 〕━━━╮
👤 {message.from_user.mention}
🆔 `{user_id}`
━━━━━━━━━━━━━━━━━━━
{chr(10).join(changes)}
╰━━━━━━━━━━━━━━━━━━━╯
"""

        await message.reply_text(msg)

        # 👉 ek hi baar update
        await add_userdata(
            user_id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            bio
        )


# ================== COMMAND ==================

@app.on_message(filters.group & filters.command("imposter") & ~filters.bot & ~filters.via_bot & admin_filter)
async def set_mataa(_, message: Message):

    if len(message.command) == 1:
        return await message.reply(
            "⚙️ Usage:\n`/imposter enable` or `/imposter disable`"
        )

    cmd = message.command[1].lower()

    if cmd == "enable":
        status = await check_pretender(message.chat.id)

        if status:
            return await message.reply("✅ Already enabled.")

        await impo_on(message.chat.id)
        await message.reply(f"🟢 Enabled in **{message.chat.title}**")

    elif cmd == "disable":
        status = await check_pretender(message.chat.id)

        if not status:
            return await message.reply("❌ Already disabled.")

        await impo_off(message.chat.id)
        await message.reply(f"🔴 Disabled in **{message.chat.title}**")

    else:
        await message.reply("⚠️ Use: `/imposter enable` or `/imposter disable`")
