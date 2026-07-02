
# ======================================================================
# ||                                                               ||
# ||   ██████╗  █████╗ ██████╗ ██╗   ██╗███████╗███████╗██╗ ██████╗  ||
# ||   ██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔════╝██╔════╝██║██╔═══██╗ ||
# ||   ██████╔╝███████║██████╔╝██║   ██║█████╗  ███████╗██║██║   ██║ ||
# ||   ██╔══██╗██╔══██║██╔══██╗██║   ██║██╔══╝  ╚════██║██║██║▄▄ ██║ ||
# ||   ██████╔╝██║  ██║██████╔╝╚██████╔╝███████╗███████║██║╚██████╔╝ ||
# ||   ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝ ╚══▀▀═╝  ||
# ║    ▓▒░ b a b i e sＩＱ ░▒▓  s e c u r e  ▓▒░ n e t w o r k ░▒▓    ║
# ||                                                               ||
# ======================================================================
# || PROJECT  : SPOTIFY_MUSIC Public Music Repository                  ||
# || AUTHOR   : BabiesIQ Team                                      ||
# || REPO     : github.com/BABY-MUSIC/SPOTIFY_MUSIC                ||
# || API      : www.babyapi.pro                                    ||
# || TELEGRAM : t.me/BabiesIQ                                      ||
# ----------------------------------------------------------------------
# || LEGAL NOTICE                                                  ||
# || Use / upload / modify at your own risk.                       ||
# || Only config /.env edit allowed.                               ||
# || Do not modify core files.                                     ||
# || Keep this header if forked.                                   ||
# || Dev not responsible for ban / damage / api block.             ||
# ----------------------------------------------------------------------
# || SECURITY                                                      ||
# || Internal protection may exist.                                ||
# || Unauthorized change may stop system.                          ||
# || Use official API only -> www.babyapi.pro                      ||
# ======================================================================


HELP_1 = """<B><u>admin commands :</b></u>

just add <b>c</b> in the starting of the commands to use them for channel.


/pause : pause the current playing stream.

/resume : resume the paused stream.

/skip : skip the current playing stream and start streaming the next track in queue.

/end or /stop : clears the queue and end the current playing stream.

/player : get a interactive player panel.

/queue : shows the queued tracks list.
"""

HELP_2 = """
<B><u>auth users :</b></u>

auth users can use admin rights in the bot without admin rights in the chat.

/auth [username/user_id] : add a user to auth list of the bot.
/unauth [username/user_id] : remove a auth users from the auth users list.
/authusers : shows the list of auth users of the group.
"""

HELP_3 = """
<U><b>broadcast feature</b></u> [only for sudoers] :

/broadcast [message or reply to a message] : broadcast a message to served chats of the bot.

<u>broadcasting modes :</u>
<b>-pin</b> : pins your broadcasted messages in served chats.
<b>-pinloud</b> : pins your broadcasted message in served chats and send notification to the members.
<b>-user</b> : broadcasts the message to the users who have started your bot.
<b>-assistant</b> : broadcast your message from the assitant account of the bot.
<b>-nobot</b> : forces the bot to not broadcast the message..

<b>example:</b> <code>/broadcast -user -assistant -pin testing broadcast</code>
"""

HELP_4 = """<U><b>chat blacklist feature :</b></u> [only for sudoers]

restrict shit chats to use our precious bot.

/blacklistchat [chat id] : blacklist a chat from using the bot.
/whitelistchat [chat id] : whitelist the blacklisted chat.
/blacklistedchat : shows the list of blacklisted chats.
"""

HELP_5 = """
<U><b>block users:</b></u> [only for sudoers]

starts ignoring the blacklisted user, so that he can't use bot commands.

/block [username or reply to a user] : block the user from our bot.
/unblock [username or reply to a user] : unblocks the blocked user.
/blockedusers : shows the list of blocked users.
"""

HELP_6 = """
<U><b>channel play commands:</b></u>

you can stream audio/video in channel.

/cplay : starts streaming the requested audio track on channel's videochat.
/cvplay : starts streaming the requested video track on channel's videochat.
/cplayforce or /cvplayforce : stops the ongoing stream and starts streaming the requested track.

/channelplay [chat username or id] or [disable] : connect channel to a group and starts streaming tracks by the help of commands sent in group.
"""

HELP_7 = """
<U><b>global ban feature</b></u> [only for sudoers] :

/gban [username or reply to a user] : globally bans the chutiya from all the served chats and blacklist him from using the bot.
/ungban [username or reply to a user] : globally unbans the globally banned user.
/gbannedusers : shows the list of globally banned users.
"""

HELP_8 = """
<B><u>loop stream :</b></u>

<b>starts streaming the ongoing stream in loop</b>

/loop [enable/disable] : enables/disables loop for the ongoing stream
/loop [1, 2, 3, ...] : enables the loop for the given value.
"""

HELP_9 = """
<U><b>maintenance mode</b></u> [only for sudoers] :

/logs : get logs of the bot.

/logger [enable/disable] : bot will start logging the activities happen on bot.

/maintenance [enable/disable] : enable or disable the maintenance mode of your bot.
"""

HELP_10 = """
<B><u>ping & stats :</b></u>

/start : starts the music bot.
/help : get help menu with explanation of commands.

/ping : shows the ping and system stats of the bot.

/stats : shows the overall stats of the bot.
"""

HELP_11 = """
<U><b>play commands :</b></u>

<b>v :</b> stands for video play.
<b>force :</b> stands for force play.

/play or /vplay : starts streaming the requested track on videochat.

/playforce or /vplayforce : stops the ongoing stream and starts streaming the requested track.
"""

HELP_12 = """
<B><u>shuffle ǫueue :</b></u>

/shuffle : shuffle's the ǫueue.
/queue : shows the shuffled ǫueue.
"""

HELP_13 = """
<B><u>seek stream :</b></u>

/seek [duration in seconds] : seek the stream to the given duration.
/seekback [duration in seconds] : backward seek the stream to the the given duration.
"""

HELP_14 = """
<B><u>song download</b></u>

/song [song name/yt url] : download any track from youtube in mp3 or mp4 formats.
"""

HELP_15 = """
<B><u>speed commands :</b></u>

you can control the playback speed of the ongoing stream. [admins only]

/speed or /playback : for adjusting the audio playback speed in group.
/cspeed or /cplayback : for adjusting the audio playback speed in channel.
"""