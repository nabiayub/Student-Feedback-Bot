from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing import assert_warns_message

from src.bot.users.keyboards import Profile
from src.bot.users.keyboards.utils import asks_yes_or_no
from src.bot.users.states import UserNameState
from src.bot.users.utils import go_to_main_menu
from src.services.repositories.users import UserRepository

router = Router()


@router.callback_query(StateFilter(UserNameState), F.data == 'skip_setting_name')
async def skip_name(
        callback_query: CallbackQuery,
        state: FSMContext,
        session_with_commit: AsyncSession) -> None:
    """
    Cancels setting name
    """
    await state.clear()
    await callback_query.answer()
    await callback_query.message.delete()

    user_repo = UserRepository(session_with_commit)
    await user_repo.set_name_and_registered_for_user(callback_query.from_user.id)


    await go_to_main_menu(
        user_tg=callback_query.from_user,
        chat_id=callback_query.from_user.id,
        bot=callback_query.message.bot,
        state=state,
        session_with_commit=session_with_commit
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
        reply_markup=asks_yes_or_no()

    )

    await state.set_state(UserNameState.CONFIRM_NAME)


@router.message(UserNameState.CONFIRM_NAME, F.text.casefold().in_({"yes", "no"}))
async def set_name(
        message: Message,
        state: FSMContext,
        session_with_commit: AsyncSession
) -> None:
    """
    Saves name and registered=True to db
    """

    user_repo = UserRepository(session_with_commit)
    telegram_id = message.from_user.id

    if message.text.casefold() == 'no':
        await user_repo.set_name_and_registered_for_user(
            telegram_id=telegram_id,
        )

    elif message.text.casefold() == 'yes':
        name = (await state.get_data()).get('name')

        await user_repo.set_name_and_registered_for_user(
            telegram_id=telegram_id,
            name=name
        )

        text = f'Your name have been successfully set to {name}.!'
        await message.answer(
            text=text,
            reply_markup=ReplyKeyboardRemove()
        )

    await state.clear()

    await go_to_main_menu(
        user_tg=message.from_user,
        chat_id=message.from_user.id,
        bot=message.bot,
        state=state,
        session_with_commit=session_with_commit
    )
