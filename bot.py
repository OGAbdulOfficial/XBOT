import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN

# Logging setup
logging.basicConfig(level=logging.INFO)

# Init Bot
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Import Handlers
from handlers.start import register_start_handlers
from handlers.user import register_user_handlers
from handlers.admin import register_admin_handlers

# Register
register_start_handlers(dp)
register_user_handlers(dp)
register_admin_handlers(dp)

async def on_startup(_):
    print("Bot is running...")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
