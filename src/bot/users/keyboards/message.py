from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy import Boolean


def ask_category_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Feedback')
    keyboard.button(text='Complaint')
    keyboard.button(text='Suggestion')
    keyboard.button(text='Go to main menu')

    keyboard.adjust(3, 1)

    return keyboard.as_markup(resize_keyboard=True)


def asks_yes_or_no(show_back: bool = False, show_main_menu: bool = False) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Yes')
    keyboard.button(text='No')

    if show_back:
        keyboard.button(text='Go back')

    if show_main_menu:
        keyboard.button(text='Go to main menu')

    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)


def go_to_main_menu_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Go to main menu')

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True)


def go_back_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='Go back')

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True)

