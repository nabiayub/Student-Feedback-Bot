from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.admin.keyboards.admin_menu_kb import admin_menu_kb
from src.bot.lexicon import MainMenuButtons, GoBackButtons

router = Router()


@router.message(F.text == MainMenuButtons.ADMIN_PANEL)
async def admin_panel(
        message: Message,
        state: FSMContext,
):
    await state.clear()

    text = (
        f"<b>🏠 Admin Panel</b>\n\n"
        f"<i>Please select a section below 👇 </i>"
    )

    await message.answer(
        text=text,
        reply_markup=admin_menu_kb()
    )


@router.message(F.text == GoBackButtons.RETURN_TO_ADMIN_PANEL)
async def go_back_to_main_menu(
        message: Message,
        state: FSMContext,
):
    await state.clear()

    await admin_panel(
        message=message,
        state=state,
    )
