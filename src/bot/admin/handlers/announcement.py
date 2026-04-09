from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.admin.handlers.start import admin_panel
from src.bot.admin.keyboards.admin_menu_kb import go_to_admin_menu_kb
from src.bot.admin.services.broadcast_message import broadcast_to_all_users
from src.bot.lexicon import AdminMenuButtons, AdminAnnouncementButtons

from src.bot.admin.states import AnnouncementState
from src.bot.users.keyboards.utils import asks_yes_or_no
from src.schemas.announcements import AnnouncementCreate
from src.schemas.users import UserCreate
from src.services.repositories.announcement import AnnouncementRepo
from src.services.repositories.users import UserRepository

router = Router()


@router.message(F.text == AdminMenuButtons.POST_ANNOUNCEMENT)
async def ask_announcement(
        message: Message,
        state: FSMContext,
) -> None:
    """Handler that asks admin to write announcement"""
    text = ("📝 <b>Announcement Draft</b>\n\n"
            "Please type the message you want to send to <b>all users</b>.")

    await message.answer(
        text=text,
        reply_markup=go_to_admin_menu_kb()
    )

    await state.set_state(AnnouncementState.ANNOUNCEMENT_TEXT)


@router.message(AnnouncementState.ANNOUNCEMENT_TEXT)
async def confirm_sending_announcement(
        message: Message,
        state: FSMContext,
) -> None:
    """Handler that asks admin to confirm sending announcement"""
    await state.update_data({'announcement_text': message.text})

    text = (f'📤 Confirm: would you like to send this announcement to all <b>users</b>?\n'
            f"━━━━━━━━━━━━━━━\n"
            f'{message.text}')

    await message.answer(
        text=text,
        reply_markup=asks_yes_or_no(
            yes_text=AdminAnnouncementButtons.CONFIRM_ANNOUNCEMENT.value,
            no_text=AdminAnnouncementButtons.CANCEL_ANNOUNCEMENT.value,
        )
    )

    await state.set_state(AnnouncementState.CONFIRM_ANNOUNCEMENT)


@router.message(AnnouncementState.CONFIRM_ANNOUNCEMENT, F.text.in_(
    {AdminAnnouncementButtons.CONFIRM_ANNOUNCEMENT,
     AdminAnnouncementButtons.CANCEL_ANNOUNCEMENT,
     })
                )
async def send_announcement(
        message: Message,
        state: FSMContext,
        session_without_commit: AsyncSession,
        session_with_commit: AsyncSession,
) -> None:
    text = message.text

    match text:
        case AdminAnnouncementButtons.GO_BACK:
            await message.answer(
                "📝 <b>Announcement Draft</b>\n\n"
                "Please type the message you want to send to <b>all users</b>.\n\n"
            )

            await state.set_state(AnnouncementState.ANNOUNCEMENT_TEXT)

        case AdminAnnouncementButtons.CANCEL_ANNOUNCEMENT:
            text = '🗑️ <b>Cancelled.</b> Your announcement hasn\'t been sent.'
            await message.answer(
                text=text,
            )

        case AdminAnnouncementButtons.CONFIRM_ANNOUNCEMENT:
            user_repo = UserRepository(session_without_commit)

            user_ids = await user_repo.get_all_users_telegram_id()
            text_for_users = (await state.get_data()).get('announcement_text')

            users_sent = await broadcast_to_all_users(
                bot=message.bot,
                user_ids=user_ids,
                text=text_for_users,
            )

            await message.answer(
                "<b>🚀 Success!</b>\n"
                f"The announcement has been pushed to <b>{users_sent}</b> users.",
            )


            announcement_message = AnnouncementCreate(
                content=text_for_users,
                sent_users=users_sent,
                telegram_id=message.from_user.id
            )

            announcement_repo = AnnouncementRepo(session_with_commit)
            await announcement_repo.create_announcement(announcement_message)

    await state.clear()

    await admin_panel(
        message=message,
        state=state
    )
