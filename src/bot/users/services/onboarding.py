from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message

from src.bot.users.keyboards import cancel_name_kb
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

    async def process_start(self, message: Message, state: FSMContext) -> None:
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

        user: User = await self.create_user_if_not_exists(
            username=username,
            telegram_id=telegram_id,
        )

        # asks user to write their name if it doesn't exist (only once at first registration)
        if not user.name and not user.registered:
            await self.set_name(
                message=message,
                state=state,
            )


    async def create_user_if_not_exists(self, username, telegram_id) -> User:
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
            reply_markup=cancel_name_kb()
        )
        await state.set_state(UserNameState.NAME)
