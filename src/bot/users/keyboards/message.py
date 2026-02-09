from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy import Boolean


def ask_category_kb() -> ReplyKeyboardMarkup:
    """
    Keyboard to display buttons with categories:
    Feedback, Complaint, Suggestion, Go to main menu
    :return:
    """
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Feedback')
    keyboard.button(text='Complaint')
    keyboard.button(text='Suggestion')
    keyboard.button(text='⬅️ Back to Menu')

    keyboard.adjust(3, 1)

    return keyboard.as_markup(resize_keyboard=True)


def go_back_kb() -> ReplyKeyboardMarkup:
    """
    Go back keyboard
    :return:
    """
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='⬅️ Go back')

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True)
