from pyrogram import filters
from pyrogram.types import Message

from BABYMUSIC import YouTube, app
from BABYMUSIC.core.call import JARVIS
from BABYMUSIC.misc import db
from BABYMUSIC.utils import AdminRightsCheck, seconds_to_min
from BABYMUSIC.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(
    filters.command(["seek", "cseek", "seekback", "cseekback"])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def seek_comm(cli, message: Message, _, chat_id):
    if len(message.command) == 1:
        return await message.reply_text(_["admin_20"])
    query = message.text.split(None, 1)[1].strip()
    if not query.isnumeric():
        return await message.reply_text(_["admin_21"])
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text(_["queue_2"])
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text(_["admin_22"])
    file_path = playing[0]["file"]
    duration_played = int(playing[0]["played"])
    duration_to_skip = int(query)
    duration = playing[0]["dur"]
    if message.command[0][-2] == "c":
        if (duration_played - duration_to_skip) <= 10:
            return await message.reply_text(
                text=_["admin_23"].format(seconds_to_min(duration_played), duration),
                reply_markup=close_markup(_),
            )
        to_seek = duration_played - duration_to_skip + 1
    else:
        if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
            return await message.reply_text(
                text=_["admin_23"].format(seconds_to_min(duration_played), duration),
                reply_markup=close_markup(_),
            )
        to_seek = duration_played + duration_to_skip + 1
    mystic = await message.reply_text(_["admin_24"])
    if "vid_" in file_path:
        n, file_path = await YouTube.video(playing[0]["vidid"], True)
        if n == 0:
            return await message.reply_text(_["admin_22"])
    check = (playing[0]).get("speed_path")
    if check:
        file_path = check
    if "index_" in file_path:
        file_path = playing[0]["vidid"]
    try:
        await JARVIS.seek_stream(
            chat_id,
            file_path,
            seconds_to_min(to_seek),
            duration,
            playing[0]["streamtype"],
        )
    except:
        return await mystic.edit_text(_["admin_26"], reply_markup=close_markup(_))
    if message.command[0][-2] == "c":
        db[chat_id][0]["played"] -= duration_to_skip
    else:
        db[chat_id][0]["played"] += duration_to_skip
    await mystic.edit_text(
        text=_["admin_25"].format(seconds_to_min(to_seek), message.from_user.mention),
        reply_markup=close_markup(_),
    )


from pyrogram import filters
from pyrogram.types import CallbackQuery

@app.on_callback_query(filters.regex(r"^SEEK"))
@AdminRightsCheck
async def seek_callback(cli, query: CallbackQuery, _, chat_id):
    data = query.data.split("|")

    if len(data) < 3:
        return await query.answer("Invalid Data", show_alert=True)

    action = data[1]  # +30 or -30

    playing = db.get(chat_id)
    if not playing:
        return await query.answer(_["queue_2"], show_alert=True)

    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await query.answer(_["admin_22"], show_alert=True)

    file_path = playing[0]["file"]
    duration_played = int(playing[0]["played"])
    duration = playing[0]["dur"]

    duration_to_skip = abs(int(action))

    # 🔁 BACKWARD
    if action.startswith("-"):
        if (duration_played - duration_to_skip) <= 10:
            return await query.answer("Can't seek back more", show_alert=True)

        to_seek = duration_played - duration_to_skip + 1

    # ⏩ FORWARD
    else:
        if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
            return await query.answer("Can't seek forward more", show_alert=True)

        to_seek = duration_played + duration_to_skip + 1

    # 🔥 Resolve file_path
    if "vid_" in file_path:
        n, file_path = await YouTube.video(playing[0]["vidid"], True)
        if n == 0:
            return await query.answer("Error", show_alert=True)

    check = playing[0].get("speed_path")
    if check:
        file_path = check

    if "index_" in file_path:
        file_path = playing[0]["vidid"]

    try:
        await JARVIS.seek_stream(
            chat_id,
            file_path,
            seconds_to_min(to_seek),
            duration,
            playing[0]["streamtype"],
        )
    except:
        return await query.answer("Seek failed", show_alert=True)

    # ✅ DB update
    if action.startswith("-"):
        db[chat_id][0]["played"] -= duration_to_skip
    else:
        db[chat_id][0]["played"] += duration_to_skip

    await query.answer(f"Seeked to {seconds_to_min(to_seek)}")
