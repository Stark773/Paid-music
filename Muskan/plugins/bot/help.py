from typing import Union
import random

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message, InputMediaPhoto

from Muskan import app
from Muskan.utils import help_pannel
from Muskan.utils.database import get_lang
from Muskan.utils.decorators.language import LanguageStart, languageCB
from Muskan.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers
from Muskan.utils.stuffs.buttons import BUTTONS
from Muskan.utils.stuffs.helper import Helper

import config

HELP_CAPTION = (
    "**╔══「 📖 Mᴜsᴋᴀɴ ʜᴇʟᴘ ᴄᴇɴᴛᴇʀ 」══╗**\n\n"
    "🎯 **sᴇʟᴇᴄᴛ ʏᴏᴜʀ ʜᴇʟᴘ ᴄᴀᴛᴇɢᴏʀʏ** ʙᴇʟᴏᴡ\n\n"
    "💬 ᴀsᴋ ᴅᴏᴜʙᴛs ᴀᴛ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ]({0})\n"
    "📌 ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴜsᴇ ᴘʀᴇғɪx : <code>/</code>\n\n"
    "**╚══「 🎵 Mᴜsᴋᴀɴ Mᴜsɪᴄ 」══╝**"
)

START_IMG = [
    "https://files.catbox.moe/x5lytj.jpg",
    "https://files.catbox.moe/psya34.jpg",
    "https://files.catbox.moe/leaexg.jpg",
    "https://files.catbox.moe/b0e4vk.jpg",
    "https://files.catbox.moe/1b1wap.jpg",
    "https://files.catbox.moe/ommjjk.jpg",
    "https://files.catbox.moe/onurxm.jpg",
    "https://files.catbox.moe/97v75k.jpg",
    "https://files.catbox.moe/t833zy.jpg",
    "https://files.catbox.moe/472piq.jpg",
    "https://files.catbox.moe/qwjeyk.jpg",
    "https://files.catbox.moe/t0hopv.jpg",
    "https://files.catbox.moe/u5ux0j.jpg",
    "https://files.catbox.moe/h1yk4w.jpg",
    "https://files.catbox.moe/gl5rg8.jpg",
]


@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        await update.edit_message_text(
            HELP_CAPTION.format(SUPPORT_CHAT),
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=HELP_CAPTION.format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(
        "📖 **ɢᴇᴛ ʜᴇʟᴘ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ** ↗️\n\nᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


@app.on_callback_query(filters.regex("setup_cb") & ~BANNED_USERS)
async def setup_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_GCSETUP,
        reply_markup=InlineKeyboardMarkup(BUTTONS.INFO_NEW),
    )


@app.on_callback_query(filters.regex("wel_cb") & ~BANNED_USERS)
async def wel_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_WEL,
        reply_markup=InlineKeyboardMarkup(BUTTONS.INFO_NEW),
    )


@app.on_callback_query(filters.regex("ad_cb") & ~BANNED_USERS)
async def ad_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_ADMIN,
        reply_markup=InlineKeyboardMarkup(BUTTONS.INFO_NEW),
    )


@app.on_callback_query(filters.regex("mod_cb") & ~BANNED_USERS)
async def mod_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_MOD,
        reply_markup=InlineKeyboardMarkup(BUTTONS.INFO_NEW),
    )


@app.on_callback_query(filters.regex("vc_cb") & ~BANNED_USERS)
async def vc_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_VC,
        reply_markup=InlineKeyboardMarkup(BUTTONS.INFO_NEW),
    )


@app.on_callback_query(filters.regex("ban_cb") & ~BANNED_USERS)
async def ban_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_BAN,
        reply_markup=InlineKeyboardMarkup(BUTTONS.INFO_NEW),
    )


@app.on_callback_query(filters.regex("abot_cb") & ~BANNED_USERS)
async def abot_cb(client, CallbackQuery):
    bot = await client.get_me()
    bot_mention = bot.mention
    await CallbackQuery.edit_message_text(
        Helper.HELP_ABOUT.format(bot_mention),
        reply_markup=InlineKeyboardMarkup(BUTTONS.INFO_BUTTON),
    )


@app.on_callback_query(filters.regex("sbot_cb") & ~BANNED_USERS)
async def sbot_cb(client, CallbackQuery):
    bot = await client.get_me()
    bot_mention = bot.mention
    await CallbackQuery.edit_message_text(
        Helper.HELP_SUPPORT.format(bot_mention),
        reply_markup=InlineKeyboardMarkup(BUTTONS.ABUTTON),
    )


@app.on_callback_query(filters.regex("ibot_cb") & ~BANNED_USERS)
async def ibot_cb(client, CallbackQuery):
    bot = await client.get_me()
    bot_mention = bot.mention
    await CallbackQuery.edit_message_text(
        Helper.HELP_INFO.format(bot_mention),
        reply_markup=InlineKeyboardMarkup(BUTTONS.INFO_BUTTON),
    )


@app.on_callback_query(filters.regex("back_cb") & ~BANNED_USERS)
async def back_cb(client, CallbackQuery):
    photo = random.choice(START_IMG)
    bot = await client.get_me()
    bot_mention = bot.mention
    await CallbackQuery.edit_message_media(
        media=InputMediaPhoto(
            media=photo,
            caption=Helper.HELP_ABOUT.format(bot_mention),
        ),
        reply_markup=InlineKeyboardMarkup(BUTTONS.INFO_BUTTON),
    )


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def help_category_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)
    help_map = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4,
        "hb5": helpers.HELP_5,
        "hb6": helpers.HELP_6,
        "hb7": helpers.HELP_7,
        "hb8": helpers.HELP_8,
        "hb9": helpers.HELP_9,
        "hb10": helpers.HELP_10,
        "hb11": helpers.HELP_11,
        "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13,
        "hb14": helpers.HELP_14,
        "hb15": helpers.HELP_15,
    }
    text = help_map.get(cb)
    if text:
        await CallbackQuery.edit_message_text(text, reply_markup=keyboard, disable_web_page_preview=True)
