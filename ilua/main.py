import os
from aiogram import Bot, Dispatcher
import asyncio
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
from aiogram.enums import ParseMode
from handlers.admin_router import admin_router
from handlers.user_router import user_router
bot=Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)

dp=Dispatcher()

dp.include_router(admin_router)
dp.include_router(user_router)





async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
