from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards.cancel import cancel_any_handler_kb
from src.bot.users.keyboards.menu import Menu
from src.bot.users.keyboards.message import MessageKeyboard
from src.bot.users.states import MessageState
from src.services.repositories.users import UserRepository

router = Router()


@router.message(F.text == 'Write feedback')
async def start_feedback(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Asks user to write his feedback.
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    text = 'Write your feedback:'
    await message.answer(
        text=text,
        reply_markup=cancel_any_handler_kb()
    )

    await state.set_state(MessageState.CONTENT)


@router.message(MessageState.CONTENT)
async def ask_anonymity_handler(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Asks user whether the feedback is anonymous or not.
    Saves message content to state
    :param message:
    :param state:
    :return:
    """
    await message.answer(text='Got ur message', reply_markup=ReplyKeyboardRemove())
    content = message.text
    await state.set_data({'content': content})


    text = 'Do you want the feedback sent anonymously?'
    await message.answer(
        text=text,
        reply_markup=MessageKeyboard.ask_anonymous_kb()
    )

    await state.set_state(MessageState.ANONYMOUS)


@router.message(MessageState.ANONYMOUS, F.text.casefold().in_({"yes", "no"}))
async def ask_confirmation_of_feedback(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Asks user to confirm the feedback.
    Saves message anonymity to state
    :return: None
    """
    anonymous = message.text.lower()
    print(anonymous)
    match anonymous:
        case 'yes':
            anonymous = True
        case 'no':
            anonymous = False

    await state.update_data({'anonymous': anonymous})

    text = 'Are you sure?'
    await message.answer(
        text=text,
        reply_markup=MessageKeyboard.confirm_or_skip_message_kb()
    )

    await state.set_state(MessageState.CONFIRM_MESSAGE)


@router.message(MessageState.CONFIRM_MESSAGE, F.text == 'Confirm')
async def save_feedback(
        message: types.Message,
        state: FSMContext,
        session_with_commit: AsyncSession
) -> None:
    """
    Saves feedback in DB
    :return: None
    """
    user_repo = UserRepository(session_with_commit)

    content = (await state.get_data()).get('content')
    anonymous = (await state.get_data()).get('anonymous')
    print(anonymous, content)

    text = 'You have successfully sent your feedback'
    await message.answer(
        text=text,
        reply_markup=Menu.main_menu_kb()
    )
