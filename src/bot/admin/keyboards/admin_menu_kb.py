from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from src.bot.lexicon import AdminMenuButtons, GoBackButtons


def admin_menu_kb() -> ReplyKeyboardMarkup:
    """Admin menu keyboard"""
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text=AdminMenuButtons.POST_ANNOUNCEMENT)
    keyboard.button(text=AdminMenuButtons.EXPORT_DATA)
    keyboard.button(text=GoBackButtons.BACK_TO_MENU)

    keyboard.adjust(2, 1)

    return keyboard.as_markup(resize_keyboard=True)


def go_to_admin_menu_kb() -> ReplyKeyboardMarkup:
    """Go to admin menu keyboard"""
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text=GoBackButtons.RETURN_TO_ADMIN_PANEL)
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)
