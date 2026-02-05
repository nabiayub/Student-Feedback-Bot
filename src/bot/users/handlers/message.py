from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards.menu import Menu
from src.bot.users.keyboards.utils import asks_yes_or_no, go_to_main_menu_kb
from src.bot.users.states import MessageState
from src.bot.users.utils import go_to_main_menu
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
        reply_markup=go_to_main_menu_kb()
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
    content = message.text
    await state.set_data({'content': content})

    text = 'Do you want the feedback sent anonymously?'
    await message.answer(
        text=text,
        reply_markup=asks_yes_or_no()
    )

    await state.set_state(MessageState.ANONYMOUS)


@router.message(MessageState.ANONYMOUS, F.text.casefold().in_({"yes", "no"}))
async def ask_confirmation_of_feedback(
        message: Message,
        state: FSMContext
) -> None:
    """
    Asks user to confirm the feedback.
    Saves message anonymity to state
    :return: None
    """

    anonymous = message.text.lower()
    match anonymous:
        case 'yes':
            anonymous = True
        case 'no':
            anonymous = False

    await state.update_data({'anonymous': anonymous})

    text = 'Do you want to send the feedback?'
    await message.answer(
        text=text,
        reply_markup=asks_yes_or_no()
    )

    await state.set_state(MessageState.CONFIRM_MESSAGE)


@router.message(MessageState.CONFIRM_MESSAGE, F.text.casefold().in_({"yes", "no"}))
async def save_feedback(
        message: Message,
        state: FSMContext,
        session_with_commit: AsyncSession
) -> None:
    """
    Saves feedback in DB
    :return: None
    """
    if message.text.casefold() == 'no':
        text = "Your feedback hasn't been sent."
        await message.answer(
            text=text,
            # reply_markup=Menu.main_menu_kb()
        )

    elif message.text.casefold() == 'yes':
        user_repo = UserRepository(session_with_commit)

        content = (await state.get_data()).get('content')
        anonymous = (await state.get_data()).get('anonymous')

        text = 'You have successfully sent your feedback'
        await message.answer(
            text=text,
            # reply_markup=Menu.main_menu_kb()
        )

    await state.clear()

    await go_to_main_menu(
        user_tg=message.from_user,
        chat_id=message.chat.id,
        bot=message.bot,
        state=state,
        session_with_commit=session_with_commit
    )
