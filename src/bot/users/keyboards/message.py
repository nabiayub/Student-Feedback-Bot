from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.bot.lexicon import GoBackButtons, MessageButtons


def ask_category_kb() -> ReplyKeyboardMarkup:
    """
    Keyboard to display buttons with categories:
    Feedback, Complaint, Suggestion, Go to main menu
    :return:
    """
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text=MessageButtons.FEEDBACK)
    keyboard.button(text=MessageButtons.COMPLAINT)
    keyboard.button(text=MessageButtons.SUGGESTION)
    keyboard.button(text=GoBackButtons.BACK_TO_MENU)

    keyboard.adjust(3, 1)

    return keyboard.as_markup(resize_keyboard=True)


def go_back_kb() -> ReplyKeyboardMarkup:
    """
    Go back keyboard
    :return:
    """
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text=GoBackButtons.GO_BACK)

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True)
