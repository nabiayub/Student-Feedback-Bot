

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.handlers.start import start_bot
from src.bot.users.states import UserNameState
from src.services.repositories.users import UserRepository

router = Router()

@router.callback_query(UserNameState.NAME, F.data == 'skip_name')
async def skip_name(callback_query: CallbackQuery,
                    state: FSMContext,
                    session_with_commit: AsyncSession) -> None:
    print('skipped user')
    user_repo = UserRepository(session_with_commit)
    await user_repo.set_name(callback_query.from_user.id)

    await callback_query.answer()

    await state.clear()
    await callback_query.message.delete()
    await callback_query.message.answer("Ok, I won’t ask again. Use /setname anytime.")


@router.callback_query(UserNameState.NAME, F.data == 'skip_name')
async def skip_name(callback: CallbackQuery,
                    state: FSMContext,
                    session_with_commit: AsyncSession) -> None:
    ...


