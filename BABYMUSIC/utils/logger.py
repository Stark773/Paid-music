import time

from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from BABYMUSIC import app
from BABYMUSIC.utils.database import is_on_off
from config import LOGGER_ID

# ================= CACHE =================
invite_cache = {}

# ================= GET LINK =================
async def get_group_link(chat):
    try:
        if chat.username:
            return f"https://t.me/{chat.username}"

        now = time.time()

        cached = invite_cache.get(chat.id)
        if cached and cached["expire"] > now:
            return cached["link"]

        link = await app.export_chat_invite_link(chat.id)

        invite_cache[chat.id] = {
            "link": link,
            "expire": now + 43200
        }

        return link

    except Exception as e:
        print("Invite link error:", e)
        return None

# ================= PLAY LOG =================
async def play_logs(message, streamtype, query: str = None):
    if await is_on_off(2):

        if query is None:
            try:
                query = message.text.split(None, 1)[1]
            except Exception:
                query = "—"

        chat = message.chat
        user = message.from_user

        # ===== LINK =====
        group_link = await get_group_link(chat)

        # ===== BUTTON =====
        if group_link:
            button = InlineKeyboardMarkup(
                [[InlineKeyboardButton("JOIN CHAT", url=group_link)]]
            )
        else:
            button = InlineKeyboardMarkup(
                [[InlineKeyboardButton(user.first_name, url=f"tg://user?id={user.id}")]]
            )

        # ===== PREMIUM BOX TEXT =====
        logger_text = f"""
<blockquote>
┌───────────────⟦ PLAY LOG ⟧───────────────┐
│
│  ◈ CHAT INFO
│  ├ ID        : <code>{chat.id}</code>
│  ├ NAME      : {chat.title}
│  └ USERNAME  : @{chat.username}
│
│  ◈ USER INFO
│  ├ ID        : <code>{user.id}</code>
│  ├ NAME      : {user.mention}
│  └ USERNAME  : @{user.username}
│
│  ◈ STREAM INFO
│  ├ QUERY     : {query}
│  └ TYPE      : {streamtype}
│
└──────────────────────────────────────────┘
</blockquote>
"""

        if chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=button,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print("LOGGER ERROR:", e)

        return
