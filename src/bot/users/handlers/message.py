from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.lexicon import MainMenuButtons, GoBackButtons, MessageButtons
from src.bot.users.keyboards.message import ask_category_kb, go_back_kb
from src.bot.users.keyboards.utils import asks_yes_or_no
from src.bot.users.services.onboarding import main_menu
from src.bot.users.states import MessageState
from src.config.settings import settings
from src.database import models
from src.schemas.messages import MessageCreate, MessageForTelegramGroup
from src.schemas.users import UserCreate
from src.services.repositories.messages import MessageRepo
from src.services.repositories.users import UserRepository

router = Router()


@router.message(F.text == MainMenuButtons.WRITE_FEEDBACK)
async def start_feedback_and_ask_category(
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
async def ask_anonymity(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Asks user whether the feedback is anonymous or not.
    Saves message content to state
    """
    category = message.text
    categories = {
        MessageButtons.FEEDBACK: 1,
        MessageButtons.COMPLAINT: 2,
        MessageButtons.SUGGESTION: 3
    }

    if category not in categories.keys():
        await message.answer(
            text='📂 Select a category below:',
            reply_markup=ask_category_kb()
        )

        return

    await state.update_data(category_id=categories[category], category_title=category)
    ##############################


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


@router.message(MessageState.ANONYMOUS, F.text.in_({"🔒 Anonymously", "📌 Publicly", GoBackButtons.GO_BACK}))
async def ask_content(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Receives ANONIMITY and ask user to write message content
    """
    is_anonymous = message.text
    match is_anonymous:
        case GoBackButtons.GO_BACK:
            text = '📂 Select a category below:'
            await message.answer(
                text=text,
                reply_markup=ask_category_kb()
            )
            await state.set_state(MessageState.CATEGORY_ID)
            return
        case '🔒 Anonymously':
            is_anonymous = True
        case '📌 Publicly':
            is_anonymous = False

    await state.update_data({'is_anonymous': is_anonymous})

    text = '✍️ Type your message:'
    await message.answer(
        text=text,
        reply_markup=go_back_kb()
    )
    await state.set_state(MessageState.CONTENT)


@router.message(MessageState.CONTENT)
async def ask_confirmation_of_feedback(
        message: Message,
        state: FSMContext
) -> None:
    """
    Asks user to confirm the feedback.
    Saves message anonymity to state
    """
    content = message.text

    if content == GoBackButtons.GO_BACK:
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

    await state.update_data({'content': content})
    ##############


    message_content = (await state.get_data()).get('content')
    category = (await state.get_data()).get('category_title')
    is_anonymous = '🔒 Anonymous' if (await state.get_data()).get('is_anonymous') else '📌 Named'

    text = (
        f"📤 <b>Confirm: would you like to send this message?</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"<b>{is_anonymous} — {category}</b>\n\n"
        f"<blockquote expandable>{message_content}</blockquote>"
    )
    await message.answer(
        text=text,
        reply_markup=asks_yes_or_no(
            yes_text='✅ Confirm',
            no_text='❌ Cancel',
            show_back=True
        )
    )

    await state.set_state(MessageState.CONFIRM_MESSAGE)


async def send_message_to_group_and_return_group_message_id(
        bot: Bot,
        group_message: MessageForTelegramGroup
) -> int:
    text = group_message.create_text_for_telegram_message()
    sent_message: Message = await bot.send_message(
        chat_id=settings.GROUP_CHAT_ID,
        text=text,
    )

    return sent_message.message_id


@router.message(MessageState.CONFIRM_MESSAGE, F.text.in_({"✅ Confirm", "❌ Cancel", GoBackButtons.GO_BACK}))
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
        case GoBackButtons.GO_BACK:
            text = '✍️ Type your message:'
            await message.answer(
                text=text,
                reply_markup=go_back_kb()
            )

            await state.set_state(MessageState.CONTENT)
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
            name = user.name
            category_id = (await state.get_data()).get('category_id')
            category_title = (await state.get_data()).get('category_title')
            content = (await state.get_data()).get('content')
            is_anonymous = (await state.get_data()).get('is_anonymous')

            new_message = MessageCreate(
                category_id=category_id,
                user_id=user_id,
                content=content,
                is_anonymous=is_anonymous,
            )

            message_repo = MessageRepo(session_with_commit)
            created_message: models.Message = await message_repo.create_message_and_return_message_id(message=new_message)


            group_message = MessageForTelegramGroup(
                message_id=created_message.id,
                content=content,
                name=name if not is_anonymous else 'Anonymous',
                category_title=category_title
            )
            admin_group_message_id = await send_message_to_group_and_return_group_message_id(message.bot, group_message)

            created_message.admin_group_message_id = admin_group_message_id

    await state.clear()

    await main_menu(
        chat_id=message.chat.id,
        bot=message.bot,
    )
