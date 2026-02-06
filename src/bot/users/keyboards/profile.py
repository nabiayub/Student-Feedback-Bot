from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cancel_name_kb() -> ReplyKeyboardMarkup:
    """
    Cancels setting name reply button.
    :return: ReplyKeyboardMarkup instance
    """
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Skip')

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True)

def profile_kb() -> ReplyKeyboardMarkup:
    """Keyboard for profile reply buttons: Change name and view history"""
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Change Name')
    keyboard.button(text='View History')
    keyboard.button(text='Go to main menu')

    keyboard.adjust(2, 1)

    return keyboard.as_markup(resize_keyboard=True)