import asyncio
import logging

from src.config.settings import settings
from src.database.db import async_session_maker
from src.factory import create_bot, create_dispatcher
from src.bot.router import register_all_routers
from src.bot.middlewares import register_middlewares
from src.bot.utils.admin_manager import admin_manager

async def on_startup(bot):
    """Tasks to run before polling starts."""
    # 1. Initialize the Admin Cache from DB
    async with async_session_maker() as session:
        await admin_manager.update_admins_list(session)

    all_admins: set[int] = await admin_manager.get_all_admins()
    # 2. Notify Super Adminsw
    for admin_id in all_admins:
        try:
            await bot.send_message(chat_id=admin_id, text='🚀 Bot is activated')
        except Exception as e:
            logging.error(f"Could not notify admin {admin_id}: {e}")


async def main():

    bot = create_bot()
    dp = create_dispatcher()

    # Manual registration as requested
    dp.startup.register(on_startup)

    register_middlewares(dp)
    register_all_routers(dp)


    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(e)
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
