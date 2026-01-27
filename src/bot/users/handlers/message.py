from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards.cancel import cancel_any_handler
from src.bot.users.keyboards.menu import Menu
from src.bot.users.keyboards.message import MessageKeyboard
from src.bot.users.states import MessageState
from src.services.repositories.users import UserRepository

router = Router()


@router.message(F.text == 'Write feedback')
async def send_feedback(
        message: types.Message,
        state: FSMContext
) -> None:
    text = 'Write your feedback:'
    await message.answer(
        text=text,
        reply_markup=cancel_any_handler()
    )

    await state.set_state(MessageState.MESSAGE)


@router.message(MessageState.MESSAGE)
async def confirm_feedback(
        message: types.Message,
        state: FSMContext
) -> None:
    feedback = message.text
    await state.set_data({'feedback': feedback})

    text = 'Are you sure?'
    await message.answer(
        text=text,
        reply_markup=MessageKeyboard.confirm_or_skip_message()
    )

    await state.set_state(MessageState.CONFIRM_MESSAGE)


@router.message(MessageState.CONFIRM_MESSAGE, F.text == 'Confirm')
async def confirm_feedback(
        message: types.Message,
        state: FSMContext,
        session_with_commit: AsyncSession
) -> None:
    user_repo = UserRepository(session_with_commit)

    feedback = (await state.get_data()).get('feedback')
    print(feedback)

    text = 'You have successfully sent your feedback'
    await message.answer(
        text=text,
        reply_markup=Menu.main_menu()
    )

