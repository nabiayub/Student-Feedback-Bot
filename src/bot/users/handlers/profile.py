from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards import Profile
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
    await user_repo.set_name_and_registered_for_user(message.from_user.id)

    await state.clear()
    text = "Ok, I won’t ask again. Use /setname anytime."
    await message.answer(
        text=text,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(UserNameState.NAME)
async def confirm_name(message: Message,
                       state: FSMContext
                       ) -> None:
    name = message.text

    await state.set_data({'name': name})

    text = f'Do you confirm {name}?'
    await message.answer(
        text=text,
        reply_markup=Profile.confirm_name_kb()
    )

    await state.set_state(UserNameState.CONFIRM_NAME)


@router.message(UserNameState.CONFIRM_NAME, F.text == 'Confirm')
async def set_name(message: Message,
                   state: FSMContext,
                   session_with_commit: AsyncSession) -> None:
    user_repo = UserRepository(session_with_commit)

    name = (await state.get_data()).get('name')
    telegram_id = message.from_user.id

    await user_repo.set_name_and_registered_for_user(
        telegram_id=telegram_id,
        name=name
    )

    text = f'Your name have been successfully set to {name}.!'
    await message.answer(
        text=text,
        reply_markup=ReplyKeyboardRemove()
    )
