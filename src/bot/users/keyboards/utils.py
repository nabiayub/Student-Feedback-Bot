from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from ...lexicon import MainMenuButtons, GoBackButtons, YesNoButtons


def asks_yes_or_no(
        yes_text: str = YesNoButtons.YES,
        no_text: str = YesNoButtons.NO,
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
        keyboard.button(text=GoBackButtons.GO_BACK)

    if show_main_menu:
        keyboard.button(text=GoBackButtons.BACK_TO_MENU)

    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)


def go_to_main_menu_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text=GoBackButtons.BACK_TO_MENU)

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True)


def main_menu_kb(show_admin_panel: bool) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=MainMenuButtons.WRITE_FEEDBACK)
    keyboard.button(text=MainMenuButtons.PROFILE)
    keyboard.button(text=MainMenuButtons.ABOUT)

    if show_admin_panel:
        keyboard.button(text=MainMenuButtons.ADMIN_PANEL)



    keyboard.adjust(1, 2, 1)

    return keyboard.as_markup(
        resize_keyboard=True,
        is_persistant=True,
    )
