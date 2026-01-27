from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def cancel_any_handler() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(
        text='Cancel',
    )

    keyboard.adjust(1)

    return keyboard.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )