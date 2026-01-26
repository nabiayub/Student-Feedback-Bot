from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards import cancel_name_kb
from src.bot.users.services.onboarding import OnboardingService
from src.bot.users.states import UserNameState
from src.schemas.users import UserCreate, UserRead
from src.services.repositories.users import UserRepository

router = Router()


@router.message(CommandStart())
async def start_bot(message: types.Message,
                    session_with_commit: AsyncSession,
                    state: FSMContext
                    ) -> None:
    """
    Handler for start command
    :param state: FSMContext
    :param message: Telegram Message
    :param session_with_commit: Session with commit
    :return: None
    """
    await message.answer(f'Welcome to AUT Feedback Bot.')

    onboarding_service = OnboardingService(session_with_commit)
    await onboarding_service.process_start(
        message=message,
        state=state,
    )
