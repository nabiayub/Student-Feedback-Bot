
from config.settings import settings

import asyncio

from aiogram import Bot,  Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.router import register_all_routers
from src.bot.middlewares import register_middlewares


async def main() -> None:
    """
    Entry point for telegram bot.
    :return: None
    """
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # register middlewares
    register_middlewares(dp)

    register_all_routers(dp)

    await bot.send_message(
        chat_id=settings.ADMIN_ID[0],
        text='Bot is activated'
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")


