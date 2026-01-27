from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

class Menu:
    """
    Class for menu keyboards
    """
    @staticmethod
    def main_menu_kb() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardBuilder()
        keyboard.button(text='Write feedback')
        keyboard.button(text='Profile')
        keyboard.button(text='About')


        keyboard.adjust(1, 2)

        return keyboard.as_markup(
            resize_keyboard=True,
            is_persistent=True
        )

