from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import User as TgUser
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards.utils import go_to_main_menu_kb, main_menu_kb
from src.bot.users.states import UserNameState
from src.config.settings import settings
from src.database.models import User
from src.schemas.users import UserCreate
from src.services.repositories.users import UserRepository

from src.bot.utils.admin_manager import admin_manager


class OnboardingService:
    """
    Handles user creation, username updates, and onboarding flow.
    Transport-independent (does not rely on Message/CallbackQuery).
    """

    def __init__(self, session: AsyncSession):
        self._user_repo = UserRepository(session)

    async def start_process(
        self,
        chat_id: int,
        bot: Bot
    ) -> None:
        """
        Entry point of onboarding logic.
        Can be called from message or callback handlers.
        """
        await self.main_menu(chat_id, bot)

    async def main_menu(self, chat_id: int, bot: Bot) -> None:
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
