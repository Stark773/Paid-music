from BABYMUSIC.core.mongo import mongodb

impdb = mongodb["pretender"]


# ✅ check user exists
async def usr_data(user_id: int) -> bool:
    return bool(await impdb.find_one({"user_id": user_id}))


# ✅ get user data (ALWAYS 4 values return karega)
async def get_userdata(user_id: int):
    user = await impdb.find_one({"user_id": user_id})

    if not user:
        return None, None, None, "No Bio"

    return (
        user.get("username"),
        user.get("first_name"),
        user.get("last_name"),
        user.get("bio", "No Bio"),  # 👉 default bio auto handle
    )


# ✅ add/update user data (bio included, but optional safe)
async def add_userdata(user_id: int, username, first_name, last_name, bio="No Bio"):
    await impdb.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "bio": bio,  # 👉 new field
            }
        },
        upsert=True,
    )


# ================== TOGGLE SYSTEM ==================

async def check_pretender(chat_id: int) -> bool:
    data = await impdb.find_one({"chat_id_toggle": chat_id})
    return False if data else True   # default ON


async def impo_on(chat_id: int):
    await impdb.delete_one({"chat_id_toggle": chat_id})  # ON


async def impo_off(chat_id: int):
    await impdb.update_one(
        {"chat_id_toggle": chat_id},
        {"$set": {"chat_id_toggle": chat_id}},
        upsert=True
    )  # OFF
