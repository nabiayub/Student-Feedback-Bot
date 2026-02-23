from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from src.bot.lexicon import AdminMenuButtons, AdminAnnouncementButtons


def admin_menu_kb() -> ReplyKeyboardMarkup:
    """Admin menu keyboard"""
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text=AdminMenuButtons.POST_ANNOUNCEMENT)
    keyboard.button(text=AdminMenuButtons.ANALYTICS)

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True)

def cancel_kb() -> ReplyKeyboardMarkup:
    """Cancel announce keyboard"""
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text=AdminAnnouncementButtons.GO_BACK)

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True)

