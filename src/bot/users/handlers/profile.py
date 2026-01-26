from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards import confirm_name_kb
from src.bot.users.states import UserNameState
from src.services.repositories.users import UserRepository

router = Router()


@router.message(StateFilter(UserNameState), F.text == 'Skip')
async def skip_name(message: Message,
                    state: FSMContext,
                    session_with_commit: AsyncSession) -> None:
    """
    Cancels setting name
    :param message: Message instance
    :param state: FSMContext
    :param session_with_commit:  Session with commit class
    :return: None
    """
    user_repo = UserRepository(session_with_commit)
    await user_repo.set_name(message.from_user.id)

    await state.clear()
    text = "Ok, I won’t ask again. Use /setname anytime."
    await message.answer(text=text)


@router.message(UserNameState.NAME)
async def set_name(message: Message,
                   state: FSMContext
                   ) -> None:
    name = message.text

    await state.set_data({'name': name})

    text = f'Do you confirm {name}?'
    await message.answer(
        text=text,
        reply_markup=confirm_name_kb()
    )

    await state.set_state(UserNameState.CONFIRM_NAME)


