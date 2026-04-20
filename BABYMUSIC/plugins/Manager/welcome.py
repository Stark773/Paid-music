import os
from pyrogram import enums, filters
from pyrogram.types import Message, ChatMemberUpdated
from pyrogram.errors import TopicClosed
from BABYMUSIC import app
from BABYMUSIC.mongo.welcomedb import is_on, set_state, bump, cool, auto_on

JOIN_THRESHOLD = 20
TIME_WINDOW = 10
COOL_MINUTES = 5
WELCOME_LIMIT = 5

last_messages: dict[int, list] = {}


def _cooldown_minutes(burst: int, threshold: int = JOIN_THRESHOLD, base: int = COOL_MINUTES) -> int:
    if burst < threshold:
        return 0
    extra = max(0, burst - threshold)
    return min(60, base + extra * 2)


@app.on_message(filters.command("welcome") & filters.group)
async def toggle(client, m: Message):
    usage = "**Usage:**\n⦿ /welcome [on|off]"
    
    if len(m.command) != 2:
        return await m.reply_text(usage)

    u = await client.get_chat_member(m.chat.id, m.from_user.id)
    if u.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await m.reply_text("**Only admins can change welcome settings!**")

    flag = m.command[1].lower()
    if flag not in ("on", "off"):
        return await m.reply_text(usage)

    cur = await is_on(m.chat.id)

    if flag == "off" and not cur:
        return await m.reply_text("**Welcome already disabled!**")
    if flag == "on" and cur:
        return await m.reply_text("**Welcome already enabled!**")

    await set_state(m.chat.id, flag)
    await m.reply_text(f"**Welcome {'enabled' if flag == 'on' else 'disabled'} in {m.chat.title}**")


@app.on_chat_member_updated(filters.group, group=-3)
async def welcome(client, update: ChatMemberUpdated):
    old = update.old_chat_member
    new = update.new_chat_member
    cid = update.chat.id

    if not (new and new.status == enums.ChatMemberStatus.MEMBER):
        return

    valid_old = (enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED)
    if old and (old.status not in valid_old):
        return

    if not await is_on(cid):
        if await auto_on(cid):
            try:
                await client.send_message(cid, "✨ Welcome system auto-enabled.")
            except TopicClosed:
                return
        else:
            return

    burst = await bump(cid, TIME_WINDOW)
    if burst >= JOIN_THRESHOLD:
        minutes = _cooldown_minutes(burst)
        await cool(cid, minutes)
        try:
            return await client.send_message(
                cid,
                f"⚠️ Mass join detected ({burst}). Welcome paused for {minutes} minutes."
            )
        except TopicClosed:
            return

    user = new.user

    try:
        # ✅ UPDATED SIMPLE WELCOME MESSAGE
        text = f"Hi {user.mention} 👋 How are you doing? Welcome here 🎶"

        sent = await client.send_message(
            cid,
            text,
            disable_web_page_preview=True
        )

        last_messages.setdefault(cid, []).append(sent)
        if len(last_messages[cid]) > WELCOME_LIMIT:
            old_msg = last_messages[cid].pop(0)
            try:
                await old_msg.delete()
            except:
                pass

    except TopicClosed:
        return

    except Exception:
        try:
            await client.send_message(cid, f"Hi {user.mention} 👋 Welcome 🎶")
        except TopicClosed:
            return
