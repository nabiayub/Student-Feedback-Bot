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
    await message.answer(f'Welcome to AUT Feedback Bot.')

    # starting the onboarding logic
    await go_to_main_menu(
        user_tg=message.from_user,
        chat_id=message.from_user.id,
        bot=message.bot,
        state=state,
        session_with_commit=session_with_commit
    )




@router.message(F.text == 'Go to main menu')
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


