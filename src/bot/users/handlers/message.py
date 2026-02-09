from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing import assert_warns_message

from src.bot.users.keyboards.message import ask_category_kb, go_back_kb
from src.bot.users.keyboards.utils import asks_yes_or_no, main_menu_kb
from src.bot.users.states import MessageState
from src.bot.users.utils import go_to_main_menu
from src.schemas.messages import MessageCreate
from src.schemas.users import UserCreate
from src.services.repositories.messages import MessageRepo
from src.services.repositories.users import UserRepository

router = Router()


@router.message(F.text == '✍️ Write feedback')
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
    text = '📂 Select a category below:'
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
    """
    Receives category and ask user to write message content
    """
    category = message.text
    categories = {
        'Feedback': 1,
        'Complaint': 2,
        'Suggestion': 3
    }

    if category not in categories.keys():
        await message.answer(
            text='📂 Select a category below:',
            reply_markup=ask_category_kb()
        )

        return


    await state.update_data(category_id=categories[category])

    text = '✍️ Type your message:'
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
    """
    content = message.text

    if content == '⬅️ Go back':
        text = '📂 Select a category below:'
        await message.answer(
            text=text,
            reply_markup=ask_category_kb()
        )

        await state.set_state(MessageState.CATEGORY_ID)
        return

    await state.update_data({'content': content})

    # text = "🔒 Do you want to send this <i>anonymously</i>. (Your name won't be shown to the administrator)."
    text = ('<b>Choose how to send:</b>\n\n'
            '🔒 <b>Anonymously:</b> Your identity stays hidden.\n'
            '📌 <b>Publicly:</b> Your name will be shown to administrator')
    await message.answer(
        text=text,
        reply_markup=asks_yes_or_no(
            yes_text='🔒 Anonymously',
            no_text='📌 Publicly',
            show_back=True
        )
    )

    await state.set_state(MessageState.ANONYMOUS)


@router.message(MessageState.ANONYMOUS, F.text.in_({"🔒 Anonymously", "📌 Publicly", "⬅️ Go back"}))
async def ask_confirmation_of_feedback(
        message: Message,
        state: FSMContext
) -> None:
    """
    Asks user to confirm the feedback.
    Saves message anonymity to state
    """
    is_anonymous = message.text
    match is_anonymous:
        case '⬅️ Go back':
            text = '✍️ Type your message:'
            await message.answer(
                text=text,
            )

            await state.set_state(MessageState.CONTENT)
            return
        case '🔒 Anonymously':
            is_anonymous = True
        case '📌 Publicly':
            is_anonymous = False

    await state.update_data({'is_anonymous': is_anonymous})

    text = '📤 Confirm: would you like to send this message?'
    await message.answer(
        text=text,
        reply_markup=asks_yes_or_no(
            yes_text='✅ Confirm',
            no_text='❌ Cancel',
            show_back=True
        )
    )

    await state.set_state(MessageState.CONFIRM_MESSAGE)


@router.message(MessageState.CONFIRM_MESSAGE, F.text.in_({"✅ Confirm", "❌ Cancel", "⬅️ Go back"}))
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
        case '⬅️ Go back':
            text = ('<b>Choose how to send:</b>\n\n'
                    '🔒 <b>Anonymously:</b> Your identity stays hidden.\n'
                    '📎 <b>Publicly:</b> Your name will be shown to administrator')
            await message.answer(
                text=text,
                reply_markup=asks_yes_or_no(
                    yes_text='🔒 Anonymously',
                    no_text='📌 Publicly',
                    show_back=True
                )
            )

            await state.set_state(MessageState.ANONYMOUS)
            return

        case '❌ Cancel':
            text = '🗑️ <b>Cancelled.</b> Your feedback hasn\'t been sent.'
            await message.answer(
                text=text,
            )

        case '✅ Confirm':
            text = '✅ <b>Feedback Sent!</b> We appreciate your input.'
            await message.answer(
                text=text,
                reply_markup=ReplyKeyboardRemove()
            )

            user_repo = UserRepository(session_with_commit)
            user = await user_repo.get_user_by_telegram_id_or_none(message.from_user.id)
            if user is None:
                user_create = UserCreate(
                    username=message.from_user.username,
                    telegram_id=message.from_user.id)
                user = await user_repo.get_or_create_user(user_create)

            user_id: int = user.id
            category_id = (await state.get_data()).get('category_id')
            content = (await state.get_data()).get('content')
            is_anonymous = (await state.get_data()).get('is_anonymous')

            new_message = MessageCreate(
                category_id=category_id,
                user_id=user_id,
                content=content,
                is_anonymous=is_anonymous,
            )

            message_repo = MessageRepo(session_with_commit)
            await message_repo.create_message(message=new_message)


    await state.clear()

    await go_to_main_menu(
        user_tg=message.from_user,
        chat_id=message.chat.id,
        bot=message.bot,
        state=state,
        session_with_commit=session_with_commit
    )
