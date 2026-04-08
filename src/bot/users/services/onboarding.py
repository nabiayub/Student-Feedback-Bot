from aiogram import Bot

from src.bot.users.keyboards.utils import main_menu_kb
from src.config.settings import settings

from src.bot.utils.admin_manager import admin_manager


async def main_menu(chat_id: int, bot: Bot) -> None:
    # is_admin = await admin_manager.is_admin(chat_id)
    is_admin = True if chat_id in settings.ADMIN_IDS else False

    text = (
        f"<b>🏠 Main Menu</b>\n\n"
        f"<i>Please select a section below 👇 </i>"
    )

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=main_menu_kb(is_admin)
    )
