from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.users.services.onboarding import OnboardingService
from src.bot.users.utils import go_to_main_menu

router = Router()


@router.message(CommandStart())
async def start_bot(message: types.Message,
                    session_with_commit: AsyncSession,
                    state: FSMContext
                    ) -> None:
    """
    Handler for start command
    :param state: FSMContext
    :param message: Telegram Message
    :param session_with_commit: Session with commit
    :return: None
    """

    text = (
        "<b>🎓 AUT Feedback Portal</b>\n\n"
        # "────────────────────\n"
        "Welcome to the official <b>AUT</b> bot. This platform is "
        "designed for students and staff to help improve our university.\n\n"

        "<b>What can you do here?</b>\n"
        "• 📝 <b>Feedbacks:</b> General experiences.\n"
        "• ⚠️ <b>Complaints:</b> Report urgent issues.\n"
        "• 💡 <b>Suggestions:</b> Propose new ideas.\n\n"

        "<blockquote expandable>"
        "<b>🔒 Your Privacy Matters</b>\n"
        "For every submission, you choose between <b>Named</b> or <b>Anonymous</b>. "
        "If you choose Anonymous, your identity is fully protected."
        "</blockquote>\n"
        "<i>Your voice shapes our university's future.</i>"
    )

    await message.answer(text=text)

    # starting the onboarding logic
    await go_to_main_menu(
        user_tg=message.from_user,
        chat_id=message.from_user.id,
        bot=message.bot,
        state=state,
        session_with_commit=session_with_commit
    )




@router.message(F.text == '⬅️ Back to Menu')
async def go_to_main_menu_handler(
        message: types.Message,
        state: FSMContext,
        session_with_commit: AsyncSession,
        ):
    """
    Universal cancel command for any handler
    :param message: Message
    :param state: FSMContext
    :param session_with_commit: Session with commit
    :return:
    """
    await state.clear()

    await go_to_main_menu(
        user_tg=message.from_user,
        chat_id=message.chat.id,
        bot=message.bot,
        state=state,
        session_with_commit=session_with_commit
    )


