import asyncio
import logging
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramNotFound


async def broadcast_to_all(bot: Bot, user_ids: list[int], text: str) -> int:
    """
    A method for broadcasting message to all users
    :param bot: bot instance
    :param user_ids: list of all user ids
    :param text: text to send to all users
    :return: number of users that the message was sent to
    """
    count = 0
    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=text)
            count += 1
            # Wait 0.05 seconds to stay under the 30 msg/sec limit
            await asyncio.sleep(0.05)

        except TelegramRetryAfter as e:
            # If we hit the limit, wait exactly as long as Telegram says
            await asyncio.sleep(e.retry_after)
            await bot.send_message(chat_id=user_id, text=text)

        except Exception as e:
            logging.error(f"Failed to send to {user_id}: {e}")

    return count