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
        # public chat
        if chat.username:
            return f"https://t.me/{chat.username}"

        now = time.time()
        cached = invite_cache.get(chat.id)

        # ✅ valid cache
        if cached and cached["expire"] > now:
            return cached["link"]

        # ❌ expired cache
        if cached:
            invite_cache.pop(chat.id, None)

        # ✅ export new
        link = await app.export_chat_invite_link(chat.id)

        invite_cache[chat.id] = {
            "link": link,
            "expire": now + 21600  # 6 hours safe
        }

        return link

    except Exception as e:
        print("Invite link error:", e)

        # ❌ remove broken cache
        invite_cache.pop(chat.id, None)
        return None

# ================= PLAY LOG =================
async def play_logs(message, streamtype, query: str = None):

    if not await is_on_off(2):
        return

    if query is None:
        try:
            query = message.text.split(None, 1)[1]
        except:
            query = "—"

    chat = message.chat
    user = message.from_user

    # ===== LINK =====
    group_link = await get_group_link(chat)

    # ===== BUTTON =====
    if group_link:
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("OPEN CHAT", url=group_link)]]
        )
    else:
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(user.first_name, url=f"tg://user?id={user.id}")]]
        )

    # ===== ULTRA PREMIUM PANEL =====
    logger_text = f"""
<blockquote>
╔═════〔 PLAY LOG 〕═════╗

  ▸ CHAT
    ├ ID   : <code>{chat.id}</code>
    ├ NAME : {chat.title}
    └ USER : @{chat.username}

  ▸ USER
    ├ ID   : <code>{user.id}</code>
    ├ NAME : {user.mention}
    └ USER : @{user.username}

  ▸ STREAM
    ├ QUERY: {query}
    └ TYPE : {streamtype}

╚═══════════════════╝
</blockquote>
"""

    # ===== SEND =====
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
