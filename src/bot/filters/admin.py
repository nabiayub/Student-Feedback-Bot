# src/bot/filters/admin.py
from aiogram.filters import BaseFilter
from aiogram.types import Message
from src.bot.utils.admin_manager import admin_manager

class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        is_admin = await admin_manager.is_admin(message.from_user.id)
        return is_admin