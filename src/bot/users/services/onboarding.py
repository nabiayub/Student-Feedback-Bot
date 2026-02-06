from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import User as TgUser
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards.profile import cancel_name_kb
from src.bot.users.keyboards.utils import go_to_main_menu_kb, main_menu_kb
from src.bot.users.states import UserNameState
from src.database.models import User
from src.schemas.users import UserCreate
from src.services.repositories.users import UserRepository


class OnboardingService:
    """
    Handles user creation, username updates, and onboarding flow.
    Transport-independent (does not rely on Message/CallbackQuery).
    """

    def __init__(self, session: AsyncSession):
        self._user_repo = UserRepository(session)

    async def start_process(
        self,
        user_tg: TgUser,
        chat_id: int,
        state: FSMContext,
        bot: Bot
    ) -> None:
        """
        Entry point of onboarding logic.
        Can be called from message or callback handlers.
        """

        user = await self.get_or_create_user(
            username=user_tg.username,
            telegram_id=user_tg.id,
        )

        user = await self.update_username(
            new_username=user_tg.username,
            user=user,
        )

        # First-time registration
        if not user.name and not user.registered:
            await self.set_name(chat_id, state, bot)

            return

        await self.main_menu(chat_id, bot)

    async def get_or_create_user(self, username: str, telegram_id: int) -> User:
        user_create = UserCreate(username=username, telegram_id=telegram_id)
        return await self._user_repo.get_or_create_user(user_create)

    async def update_username(self, new_username: str, user: User) -> User:
        if user.username != new_username:
            user.username = new_username
            await self._user_repo.update_username(user)
        return user

    async def set_name(self, chat_id: int, state: FSMContext, bot: Bot) -> None:
        await bot.send_message(
            chat_id=chat_id,
            text="Enter your name (optional):",
            reply_markup=cancel_name_kb()
        )
        await state.set_state(UserNameState.NAME)

    async def main_menu(self, chat_id: int, bot: Bot) -> None:
        await bot.send_message(
            chat_id=chat_id,
            text="Choose your action",
            reply_markup=main_menu_kb()
        )
