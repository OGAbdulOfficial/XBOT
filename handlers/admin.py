from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import ADMIN_IDS
from database import (
    get_total_users, get_total_channels, get_channels, 
    add_channel, remove_channel, set_video, get_all_users_cursor
)
from keyboards.admin_kb import admin_panel_kb, cancel_kb
import asyncio

class AdminState(StatesGroup):
    broadcast = State()
    add_channel = State()
    remove_channel = State()
    set_video = State()

def is_admin(user_id):
    return user_id in ADMIN_IDS

async def admin_cmd(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("🛠 *Admin Panel*", reply_markup=admin_panel_kb(), parse_mode="Markdown")

async def admin_cb_handler(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        return

    action = call.data
    
    if action == "admin_stats":
        users = await get_total_users()
        channels = await get_total_channels()
        # Referrals count requires aggregation or sum, skipping complexity for speed unless crucial
        # showing basic stats
        text = (
            f"📊 *Bot Statistics*\n\n"
            f"👥 Users: {users}\n"
            f"📢 Channels: {channels}"
        )
        await call.message.answer(text, parse_mode="Markdown")
        
    elif action == "admin_broadcast":
        await AdminState.broadcast.set()
        await call.message.answer("📢 Send the message to broadcast (Text, Photo, Video, etc.)", reply_markup=cancel_kb())
        
    elif action == "admin_add_ch":
        await AdminState.add_channel.set()
        await call.message.answer("Tb add a channel, send the @username (Make sure bot is admin there).", reply_markup=cancel_kb())
        
    elif action == "admin_rem_ch":
        current = await get_channels()
        text = "➖ Send username to remove:\n" + "\n".join(current)
        await AdminState.remove_channel.set()
        await call.message.answer(text, reply_markup=cancel_kb())
        
    elif action == "admin_set_vid":
        await AdminState.set_video.set()
        await call.message.answer("🎬 Send the new Video Link (or public file link):", reply_markup=cancel_kb())
        
    elif action == "admin_close":
        await call.message.delete()
        
    elif action == "admin_cancel":
        await state.finish()
        await call.message.edit_text("❌ Cancelled", reply_markup=None)
        
    await call.answer()

async def input_broadcast(message: types.Message, state: FSMContext):
    users_cursor = await get_all_users_cursor()
    count = 0
    blocked = 0
    
    msg_to_send = await message.answer("⏳ Broadcast started...")
    
    async for user in users_cursor:
        try:
            # Copy message preserves type (photo/video/text)
            await message.copy_to(user['user_id'])
            count += 1
        except Exception:
            blocked += 1
        await asyncio.sleep(0.05) # Safe rate limit
        
    await msg_to_send.edit_text(f"✅ Broadcast Complete.\nSent: {count}\nFailed/Blocked: {blocked}")
    await state.finish()

async def input_add_channel(message: types.Message, state: FSMContext):
    ch = message.text.strip()
    # Basic validation
    if not ch.startswith("@") and not ch.startswith("-100"):
        await message.answer("⚠️ Format invalid. Use @username or ID.")
        # Don't finish state, let them retry or cancel
        return 
        
    await add_channel(ch)
    await message.answer(f"✅ Channel {ch} added to force join.")
    await state.finish()

async def input_remove_channel(message: types.Message, state: FSMContext):
    ch = message.text.strip()
    await remove_channel(ch)
    await message.answer(f"✅ Channel {ch} removed.")
    await state.finish()

async def input_set_video(message: types.Message, state: FSMContext):
    vid = message.text.strip()
    await set_video(vid)
    await message.answer("✅ Video link updated.")
    await state.finish()

async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Cancelled.")
    await call.answer()

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_cmd, commands=["admin"])
    dp.register_callback_query_handler(admin_cb_handler, text_startswith="admin_", state="*")
    
    dp.register_message_handler(input_broadcast, content_types=types.ContentTypes.ANY, state=AdminState.broadcast)
    dp.register_message_handler(input_add_channel, state=AdminState.add_channel)
    dp.register_message_handler(input_remove_channel, state=AdminState.remove_channel)
    dp.register_message_handler(input_set_video, state=AdminState.set_video)
