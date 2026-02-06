from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards.profile import profile_kb, cancel_name_kb, HistoryPaginatorCBData, get_history_paginator_cb
from src.bot.users.keyboards.utils import asks_yes_or_no, go_to_main_menu_kb
from src.bot.users.states import UserNameState
from src.bot.users.utils import go_to_main_menu
from src.bot.utils import format_history_text
from src.schemas.messages import MessageRead
from src.services.repositories.messages import MessageRepo
from src.services.repositories.users import UserRepository

router = Router()


@router.message(F.text == 'Profile')
async def profile_view(
        message: Message,
        session_without_commit: AsyncSession,
) -> None:
    user_repo = UserRepository(session_without_commit)
    user_name = await user_repo.get_name_by_telegram_id(message.from_user.id)

    text = ('Profile'
            f'Your name {user_name}\n'
            'Choose 👇')

    await message.answer(
        text=text,
        reply_markup=profile_kb()
    )


@router.message(F.text == 'Change Name')
async def start_changing_name(
        message: Message,
        state: FSMContext,
) -> None:
    await message.answer(
        text="Enter your name (optional):",
        reply_markup=cancel_name_kb()
    )
    await state.set_state(UserNameState.NAME)


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
            text = f'You did not change your name.'
            await message.answer(
                text=text,
                reply_markup=ReplyKeyboardRemove()
            )

            await user_repo.set_name_and_registered_for_user(
                telegram_id=telegram_id,
            )
        case 'Yes':
            name = (await state.get_data()).get('name')

            text = f'Your name have been successfully set to {name}!'
            await message.answer(
                text=text,
                reply_markup=ReplyKeyboardRemove()
            )

            await user_repo.set_name_and_registered_for_user(
                telegram_id=telegram_id,
                name=name
            )

    await state.clear()

    await go_to_main_menu(
        user_tg=message.from_user,
        chat_id=message.from_user.id,
        bot=message.bot,
        state=state,
        session_with_commit=session_with_commit
    )


@router.message(F.text == 'Show history')
async def show_history_first(
        message: Message,
        session_without_commit: AsyncSession,
) -> None:
    """Handler that shows history of message of users"""
    page = 1

    message_repo = MessageRepo(session_without_commit)
    messages, has_next = await message_repo.get_messages_of_one_user(
        telegram_id=message.from_user.id,
        page=page
    )

    if not messages:
        await message.answer('Your history is empty.')
        return

    text = format_history_text(messages)

    await message.answer(
        text=text,
        reply_markup=get_history_paginator_cb(
            page=page,
            has_next=has_next
        ),
    )


@router.callback_query(HistoryPaginatorCBData.filter(F.action != "ignore"))
async def process_history_pagination(
        callback: CallbackQuery,
        callback_data: HistoryPaginatorCBData,
        session_without_commit: AsyncSession,
) -> None:
    """Handler that handles the pagination of history of message of users"""
    page = callback_data.page

    message_repo = MessageRepo(session_without_commit)
    messages, has_next = await message_repo.get_messages_of_one_user(
        telegram_id=callback.from_user.id,
        page=page
    )

    text = format_history_text(messages)

    await callback.message.edit_text(
        text=text,
        reply_markup=get_history_paginator_cb(
            page=page,
            has_next=has_next
        ),
    )

    await callback.answer()
