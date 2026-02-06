from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def asks_yes_or_no(show_back: bool = False, show_main_menu: bool = False) -> ReplyKeyboardMarkup:
    """
    Keyboard that has buttons Yes or No
    :param show_back: bool - if True, shows the back button
    :param show_main_menu: bool - if True, shows the main menu
    :return:
    """
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


def main_menu_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Write feedback')
    keyboard.button(text='Profile')
    keyboard.button(text='About')

    keyboard.adjust(1, 2)

    return keyboard.as_markup(
        resize_keyboard=True,
    )
