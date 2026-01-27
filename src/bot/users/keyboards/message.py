from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MessageKeyboard:
    @staticmethod
    def asks_yes_or_no() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        keyboard.button(text='Yes', callback_data='yes')
        keyboard.button(text='No', callback_data='no')

        keyboard.adjust(2)

        return keyboard.as_markup()

