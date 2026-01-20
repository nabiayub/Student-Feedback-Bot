
from config.settings import settings, loguru_logger

import asyncio

from aiogram import Bot,  Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

async def main() -> None:
    """
    Entry point for telegram bot.
    :return: None
    """
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

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


