import asyncio
import logging

from src.config.settings import settings
from src.factory import create_bot, create_dispatcher
from src.bot.router import register_all_routers
from src.bot.middlewares import register_middlewares


async def main():

    bot = create_bot()
    dp = create_dispatcher()

    # Manual registration as requested
    register_middlewares(dp)
    register_all_routers(dp)

    # Set up Admin-specific menu
    try:
        await bot.send_message(
            chat_id=settings.ADMIN_IDS[0],
            text='Bot is activated'
        )
    except Exception as e:
        print("---------------------------------------")
        print(f"FAILED to send activation message.")
        print(f"Reason: {e}")
        print("FIX: Go to your new bot and press START.")
        print("---------------------------------------")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
