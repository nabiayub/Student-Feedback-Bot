from typing import Any, Coroutine

from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message

from src.bot.users.keyboards import Profile
from src.bot.users.keyboards.menu import Menu
from src.bot.users.states import UserNameState
from src.database.models import User
from src.schemas.users import UserCreate
from src.services.repositories.users import UserRepository


class OnboardingService:
    """
    Class for onboarding services via /start command
    """

    def __init__(self, session: AsyncSession):
        self._user_repo = UserRepository(session)

    async def start_process(self, message: Message, state: FSMContext) -> None:
        """
        Entry point for /start command.
        Ensures the user exists and starts onboarding if needed.
        :param message: Message
        :param state: FSMContext
        :return: None
        """
        ## creating user when /start if he doesn't exist
        username = message.from_user.username
        telegram_id = message.from_user.id

        user: User = await self.get_or_create_user(
            username=username,
            telegram_id=telegram_id,
        )
        user = await self.update_username(
            new_username=message.from_user.username,
            user=user,
        )

        # asks user to write their name if it doesn't exist (only once at first registration)
        if not user.name and not user.registered:
            await self.set_name(
                message=message,
                state=state
            )
        await self.main_menu(message)

    async def get_or_create_user(self, username: str, telegram_id: int) -> User:
        """
        Creates the user if not exists and returns DB user.
        username: username of telegram user
        telegram_id: telegram id of telegram user
        return: User model
        """
        user = UserCreate(
            username=username,
            telegram_id=telegram_id
        )
        db_user = await self._user_repo.get_or_create_user(user)

        return db_user

    async def update_username(self, new_username: str, user: User) -> User:
        if user.username != new_username:
            user.username = new_username
            await self._user_repo.update_username(user)
        return user

    async def set_name(self, message: Message, state: FSMContext) -> None:
        """
        For the first registration, sends message asking for name.
        :param message: Message
        :param state: FSMContext
        :return: None
        """
        text = 'Enter your name (optional):'
        await message.answer(
            text=text,
            reply_markup=Profile.cancel_name_kb()
        )
        await state.set_state(UserNameState.NAME)

    async def main_menu(self, message: Message) -> None:
        text = 'Choose your action'
        await message.answer(
            text=text,
            reply_markup=Menu.main_menu_kb())
