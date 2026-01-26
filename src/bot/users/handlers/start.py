from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards import cancel_name_kb
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

    user_repo = UserRepository(session_with_commit)
    user = UserCreate(
        username=message.from_user.username,
        telegram_id=message.from_user.id,
    )
    db_user = await user_repo.get_or_create_user(user)

    if not db_user.name and not db_user.registered:
        text = 'Enter your name (optional):'
        await message.answer(
            text=text,
            reply_markup=cancel_name_kb()
        )
        await state.set_state(UserNameState.NAME)
