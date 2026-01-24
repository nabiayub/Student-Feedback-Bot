from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import UserCreate
from src.services.repositories.users import UserRepository

router = Router()


@router.message(Command('start'))
async def start_bot(message: types.Message, session_with_commit: AsyncSession) -> None:
    """
    Handler for start command
    :param message: Telegram Message
    :param session_with_commit: Session with commit
    :return: None
    """

    await message.answer(f'Добро пожаловать в бота {message.from_user.username} ')


    user_repo = UserRepository(session_with_commit)
    user = UserCreate(
        username=message.from_user.username,
        telegram_id=message.from_user.id,
    )
    result = await user_repo.get_or_create_user(user)





