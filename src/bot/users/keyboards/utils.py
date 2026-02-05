from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def asks_yes_or_no() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Yes')
    keyboard.button(text='No')

    keyboard.adjust(2)

    return keyboard.as_markup(
        resize_keyboard=True
    )

def go_to_main_menu_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Go to main menu')

    keyboard.adjust(1)

    return keyboard.as_markup(
        resize_keyboard=True
    )
