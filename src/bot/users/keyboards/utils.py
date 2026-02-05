from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy import Boolean


def asks_yes_or_no(show_back: bool=False) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Yes')
    keyboard.button(text='No')

    if show_back:
        keyboard.button(text='Go back')

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
