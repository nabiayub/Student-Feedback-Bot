from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.keyboards.menu import Menu
from src.bot.users.keyboards.message import asks_yes_or_no, ask_category_kb, go_back_kb
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
    text = 'Choose category:'
    await message.answer(
        text=text,
        reply_markup=ask_category_kb()
    )

    await state.set_state(MessageState.CATEGORY_ID)


@router.message(MessageState.CATEGORY_ID)
async def ask_to_write_feedback(
        message: types.Message,
        state: FSMContext
) -> None:
    category = message.text
    categories = {
        'Feedback': 1,
        'Complaint': 2,
        'Suggestion': 3
    }

    await state.update_data(category_id=categories[category])

    text = 'Write your message:'
    await message.answer(
        text=text,
        reply_markup=go_back_kb()
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

    if content == 'Go back':
        text = 'Please choose category again:'
        await message.answer(
            text=text,
            reply_markup=ask_category_kb()
        )

        await state.set_state(MessageState.CATEGORY_ID)
        return

    await state.update_data({'content': content})

    text = 'Do you want the feedback sent anonymously?'
    await message.answer(
        text=text,
        reply_markup=asks_yes_or_no(show_back=True)
    )

    await state.set_state(MessageState.ANONYMOUS)


@router.message(MessageState.ANONYMOUS, F.text.in_({"Yes", "No", "Go back"}))
async def ask_confirmation_of_feedback(
        message: Message,
        state: FSMContext
) -> None:
    """
    Asks user to confirm the feedback.
    Saves message anonymity to state
    :return: None
    """
    anonymous = message.text
    match anonymous:
        case 'Go back':
            text = 'Please enter your message again:'
            await message.answer(
                text=text,
            )

            await state.set_state(MessageState.CONTENT)
            return
        case 'Yes':
            anonymous = True
        case 'No':
            anonymous = False

    await state.update_data({'anonymous': anonymous})

    text = 'Do you want to send the feedback?'
    await message.answer(
        text=text,
        reply_markup=asks_yes_or_no(show_back=True)
    )

    await state.set_state(MessageState.CONFIRM_MESSAGE)


@router.message(MessageState.CONFIRM_MESSAGE, F.text.in_({"Yes", "No", "Go back"}))
async def save_feedback(
        message: Message,
        state: FSMContext,
        session_with_commit: AsyncSession
) -> None:
    """
    Saves feedback in DB
    :return: None
    """

    response = message.text

    match response:
        case 'Go back':
            text = 'Please choose again:'
            await message.answer(
                text=text,
            )

            await state.set_state(MessageState.ANONYMOUS)
            return

        case 'No':
            text = "Your feedback hasn't been sent."
            await message.answer(
                text=text,
            )

        case 'Yes':
            user_repo = UserRepository(session_with_commit)

            category_id = (await state.get_data()).get('category_id')
            content = (await state.get_data()).get('content')
            anonymous = (await state.get_data()).get('anonymous')

            print(category_id, content, anonymous)

            text = 'You have successfully sent your feedback'
            await message.answer(
                text=text,
            )



    await state.clear()

    await go_to_main_menu(
        user_tg=message.from_user,
        chat_id=message.chat.id,
        bot=message.bot,
        state=state,
        session_with_commit=session_with_commit
    )
