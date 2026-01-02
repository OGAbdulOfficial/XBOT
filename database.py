import motor.motor_asyncio
from config import MONGO_URI

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client['xbot_viral_db']

users_col = db['users']
channels_col = db['channels']
settings_col = db['settings']

# --- USERS ---
async def add_user(user_id, ref_by=None):
    user = await users_col.find_one({"user_id": user_id})
    if not user:
        await users_col.insert_one({
            "user_id": user_id,
            "ref_by": ref_by,
            "referrals_count": 0,
            "joined_at": 0 # Timestamp can be added if needed
        })
        if ref_by:
            await users_col.update_one(
                {"user_id": ref_by},
                {"$inc": {"referrals_count": 1}}
            )

async def get_user(user_id):
    return await users_col.find_one({"user_id": user_id})

async def get_total_users():
    return await users_col.count_documents({})

async def get_all_users_cursor():
    return users_col.find({})

# --- CHANNELS (FORCE JOIN) ---
async def add_channel(channel):
    # channel should be username (e.g. @channel) or ID
    existing = await channels_col.find_one({"channel": channel})
    if not existing:
        await channels_col.insert_one({"channel": channel})

async def remove_channel(channel):
    await channels_col.delete_one({"channel": channel})

async def get_channels():
    # Returns list of channel strings
    cursor = channels_col.find({})
    channels = []
    async for document in cursor:
        channels.append(document['channel'])
    return channels

async def get_total_channels():
    return await channels_col.count_documents({})

# --- SETTINGS (VIDEO / CONFIG) ---
async def set_video(link):
    await settings_col.update_one(
        {"key": "video_link"},
        {"$set": {"value": link}},
        upsert=True
    )

async def get_video():
    doc = await settings_col.find_one({"key": "video_link"})
    return doc['value'] if doc else None
