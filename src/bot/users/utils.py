from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot
from aiogram.types import User as TgUser

from src.bot.users.services.onboarding import OnboardingService


async def go_to_main_menu(user_tg: TgUser, chat_id: int, bot: Bot, state: FSMContext, session_with_commit: AsyncSession):
    """
    Method to return to main menu
    :param user_tg: TgUser object
    :param chat_id: chat id int
    :param bot: Bot object
    :param state: FsmContext
    :param session_with_commit: session
    :return:
    """

    onboarding_service = OnboardingService(session_with_commit)
    await onboarding_service.start_process(
        user_tg=user_tg,
        chat_id=chat_id,
        state=state,
        bot=bot
    )
