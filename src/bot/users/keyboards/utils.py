from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def asks_yes_or_no(
        yes_text: str = 'Yes',
        no_text: str = 'No',
        show_back: bool = False,
        show_main_menu: bool = False
) -> ReplyKeyboardMarkup:
    """
    Keyboard that has buttons Yes or No
    :param no_text: Text to display on no button
    :param yes_text: Text to display on yes button
    :param show_back: bool - if True, shows the back button
    :param show_main_menu: bool - if True, shows the main menu
    :return:
    """
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text=f'{yes_text}')
    keyboard.button(text=f'{no_text}')

    if show_back:
        keyboard.button(text='⬅️ Go back')

    if show_main_menu:
        keyboard.button(text='⬅️ Back to Menu')

    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)


def go_to_main_menu_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='⬅️ Back to Menu')

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True)


def main_menu_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='✍️ Write feedback')
    keyboard.button(text='👤 Profile')
    keyboard.button(text='ℹ️ About')

    keyboard.adjust(1, 2)

    return keyboard.as_markup(
        resize_keyboard=True,
    )
