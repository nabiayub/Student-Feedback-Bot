from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards.utils import asks_yes_or_no, go_to_main_menu_kb
from src.bot.users.states import UserNameState
from src.bot.users.utils import go_to_main_menu
from src.services.repositories.users import UserRepository

router = Router()


@router.message(StateFilter(UserNameState), F.text == 'Skip')
async def skip_name(
        message: Message,
        state: FSMContext,
        session_with_commit: AsyncSession) -> None:
    """
    Cancels setting name
    """
    await state.clear()

    user_repo = UserRepository(session_with_commit)
    await user_repo.set_name_and_registered_for_user(message.from_user.id)


    await go_to_main_menu(
        user_tg=message.from_user,
        chat_id=message.from_user.id,
        bot=message.bot,
        state=state,
        session_with_commit=session_with_commit
    )


@router.message(UserNameState.NAME)
async def confirm_name(
        message: Message,
        state: FSMContext
) -> None:
    name = message.text

    await state.set_data({'name': name})

    text = f'Do you confirm {name}?'
    await message.answer(
        text=text,
        reply_markup=asks_yes_or_no(show_back=True)
    )

    await state.set_state(UserNameState.CONFIRM_NAME)


@router.message(UserNameState.CONFIRM_NAME, F.text.in_({"Yes", "No", "Go back"}))
async def save_name(
        message: Message,
        state: FSMContext,
        session_with_commit: AsyncSession
) -> None:
    """
    Saves name and registered=True to db
    """
    response = message.text
    if response == "Go back":
        text = "Enter your name again (optional):"
        await message.answer(
            text=text,
            reply_markup=go_to_main_menu_kb()
        )
        await state.set_state(UserNameState.NAME)

    user_repo = UserRepository(session_with_commit)
    telegram_id = message.from_user.id

    match response:
        case 'No':
            await user_repo.set_name_and_registered_for_user(
                telegram_id=telegram_id,
            )

        case 'Yes':
            name = (await state.get_data()).get('name')

            await user_repo.set_name_and_registered_for_user(
                telegram_id=telegram_id,
                name=name
            )

            text = f'Your name have been successfully set to {name}!'
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
