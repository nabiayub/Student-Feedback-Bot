
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.states import UserNameState
from src.services.repositories.users import UserRepository

router = Router()

@router.message(UserNameState.NAME, F.text == 'Skip')
async def skip_name(message: Message,
                    state: FSMContext,
                    session_with_commit: AsyncSession) -> None:

    user_repo = UserRepository(session_with_commit)
    await user_repo.set_name(message.from_user.id)

    await state.clear()
    await message.reply("Ok, I won’t ask again. Use /setname anytime.")



