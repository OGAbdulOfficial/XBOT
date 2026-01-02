from aiogram import types, Dispatcher
from database import get_video, get_user, get_total_users
from keyboards.user_kb import get_video_kb, forward_link_kb, user_main_kb

async def get_video_handler(call: types.CallbackQuery):
    video = await get_video()
    if not video:
        await call.answer("❌ Video is currently unavailable.", show_alert=True)
        return

    # Check if video is a file_id, or http link, or telegram link
    # The requirement says "Link (stored in DB)". 
    # Can send as message with button or just message.
    
    try:
        if video.startswith("http"):
             await call.message.answer(
                 "🎬 *Here is your video:*",
                 reply_markup=get_video_kb(video),
                 parse_mode="Markdown"
             )
        else:
            # Assume file_id or text
            await call.message.answer_video(video, caption="🎬 Here is your video!")
    except Exception:
         await call.message.answer(f"🎬 Access Video:\n{video}")
         
    await call.answer()

async def get_link_handler(call: types.CallbackQuery):
    bot_user = await call.bot.get_me()
    ref_link = f"https://t.me/{bot_user.username}?start={call.from_user.id}"
    
    await call.message.answer(
        f"🔗 *Your Referral Link:*\n`{ref_link}`\n\nShare this link to invite friends!",
        reply_markup=forward_link_kb(ref_link),
        parse_mode="Markdown"
    )
    await call.answer()

async def view_stats_handler(call: types.CallbackQuery):
    user_data = await get_user(call.from_user.id)
    total_refs = user_data.get('referrals_count', 0) if user_data else 0
    # Global stats usually for admin, but specific req asks "Total users" in View Stats
    # Assuming user wants to see global stats too? Req: "Total users, User's referral count"
    global_users = await get_total_users()
    
    text = (
        f"📊 *Statistics*\n\n"
        f"👤 **Your Referrals:** {total_refs}\n"
        f"🌍 **Total Users:** {global_users}"
    )
    await call.message.answer(text, parse_mode="Markdown")
    await call.answer()

def register_user_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_video_handler, text="get_video")
    dp.register_callback_query_handler(get_link_handler, text="get_link")
    dp.register_callback_query_handler(view_stats_handler, text="view_stats")
