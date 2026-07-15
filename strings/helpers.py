HELP_1 = """<b><u>🎵 Admin Commands :</u></b>

Add <b>c</b> at the start of commands to use them for channels.

/pause — Pause the current stream.
/resume — Resume the paused stream.
/skip — Skip current track and play next in queue.
/end or /stop — Clear queue and stop stream.
/queue — Show queued tracks list.
/loop [disable/enable] or [1-10] — Loop current track.
/shuffle — Shuffle the queue.
/seek — Seek stream to given duration.
/seekback — Seek stream backward.
/speed or /playback — Adjust audio playback speed.

<b>Powered by :</b> <a href="{0}">Muskan Music</a>
""".format("https://t.me/muskan_music_support")

HELP_2 = """<b><u>🔐 Auth Users :</u></b>

Auth users can use admin rights in bot without group admin rights.

/auth [username/user_id] — Add user to auth list.
/unauth [username/user_id] — Remove user from auth list.
/authusers — Show list of auth users.

<b>Powered by :</b> <a href="https://t.me/muskan_music_support">Muskan Music</a>
"""

HELP_3 = """<b><u>📢 Broadcast Feature</u></b> [Sudoers only] :

/broadcast [message or reply] — Broadcast to served chats.

<b>Broadcasting Modes :</b>

<b>-pin</b> — Pin broadcasted message in served chats.
<b>-pinloud</b> — Pin with notification.
<b>-user</b> — Broadcast to users who started the bot.
<b>-assistant</b> — Broadcast from assistant account.
<b>-nobot</b> — Force bot not to broadcast.

<b>Example :</b>
<code>/broadcast -user -assistant -pin Hello from Muskan!</code>

<b>Powered by :</b> <a href="https://t.me/muskan_music_support">Muskan Music</a>
"""

HELP_4 = """<b><u>🚫 Blacklist Feature :</u></b> [Sudoers only]

/blacklistchat [chat id] — Blacklist a chat.
/whitelistchat [chat id] — Whitelist a blacklisted chat.
/blacklistedchat — Show blacklisted chats list.

<b><u>Block Users :</u></b> [Sudoers only]

/block [username or reply] — Block user from bot.
/unblock [username or reply] — Unblock a blocked user.
/blockedusers — Show blocked users list.

<b>Powered by :</b> <a href="https://t.me/muskan_music_support">Muskan Music</a>
"""

HELP_5 = """<b><u>🎵 Play Commands :</u></b>

<b>v</b> — Video play. | <b>force</b> — Force play (skip queue).

/play [song name or link] — Play audio in voice chat.
/vplay [song name or link] — Play video in voice chat.
/cplay [song name or link] — Play audio in connected channel.
/cvplay [song name or link] — Play video in connected channel.
/playforce — Force play audio (skip queue).
/vplayforce — Force play video (skip queue).

Supported : YouTube, Spotify, Apple Music, Resso, SoundCloud, Telegram files

<b>Powered by :</b> <a href="https://t.me/muskan_music_support">Muskan Music</a>
"""

HELP_6 = """<b><u>🎛 Global Ban Feature :</u></b> [Sudoers only]

/gban [username/user_id] — Global ban a user.
/ungban [username/user_id] — Remove global ban.
/gbannedusers — Show globally banned users list.

<b>Powered by :</b> <a href="https://t.me/muskan_music_support">Muskan Music</a>
"""

HELP_7 = """<b><u>📋 Song Download :</u></b>

/song [song name or YouTube link] — Download song to private chat.

<b>Powered by :</b> <a href="https://t.me/muskan_music_support">Muskan Music</a>
"""

HELP_8 = """<b><u>⚙️ Group Setup :</u></b>

/add — Add Muskan to your group.
/leave — Ask Muskan to leave the group.
/lang — Change bot language.
/settings — Configure bot settings.
/playmode — Set play mode.

<b>Powered by :</b> <a href="https://t.me/muskan_music_support">Muskan Music</a>
"""
