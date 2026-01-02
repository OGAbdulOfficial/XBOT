from aiogram import types, Dispatcher
from database import add_user, get_channels
from keyboards.user_kb import force_join_kb, user_main_kb
from config import ADMIN_IDS, START_PIC

async def start_handler(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args()
    ref_by = None
    
    if args and args.isdigit():
        possible_ref = int(args)
        if possible_ref != user_id:
            ref_by = possible_ref
            
    await add_user(user_id, ref_by)
    
    # Check Force Join
    if not await check_force_join(message.bot, user_id):
        channels = await get_channels()
        caption = "⛔️ Mᴜsᴛ Jᴏɪɴ Oᴜʀ Aʟʟ Cʜᴀɴɴᴇʟs"
        
        try:
            await message.answer_photo(
                photo=START_PIC,
                caption=caption,
                reply_markup=force_join_kb(channels),
                parse_mode="Markdown"
            )
        except:
             await message.answer(
                caption,
                reply_markup=force_join_kb(channels),
                parse_mode="Markdown"
            )
        return

    # Welcome Screen
    caption = "🎉 *Welcome! Choose an option below*"
    try:
        await message.answer_photo(
            photo=START_PIC,
            caption=caption,
            reply_markup=user_main_kb(),
            parse_mode="Markdown"
        )
    except:
        await message.answer(
            caption,
            reply_markup=user_main_kb(),
            parse_mode="Markdown"
        )

async def check_join_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    if not await check_force_join(call.bot, user_id):
        await call.answer("❌ You haven't joined all channels yet!", show_alert=True)
        return

    await call.message.delete()
    
    caption = "🎉 *Verified!* Login Successful."
    try:
        await call.message.answer_photo(
            photo=START_PIC,
            caption=caption,
            reply_markup=user_main_kb(),
            parse_mode="Markdown"
        )
    except:
        await call.message.answer(
            caption,
            reply_markup=user_main_kb(),
            parse_mode="Markdown"
        )

async def check_force_join(bot, user_id):
    channels = await get_channels()
    if user_id in ADMIN_IDS:
        return True # Admin bypass
        
    for ch in channels:
        try:
            # Skip check for private status links or standard links
            if ch.startswith("http") or ch.startswith("t.me"):
                continue 
                
            member = await bot.get_chat_member(ch, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(f"Error checking channel {ch}: {e}")
            return False 
            
    return True

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_callback_query_handler(check_join_callback, text="check_join")
