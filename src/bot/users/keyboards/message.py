from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

class MessageKeyboard:
    @staticmethod
    def confirm_or_skip_message() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardBuilder()

        keyboard.button(text='Confirm')
        keyboard.button(text='Cancel')

        keyboard.adjust(2)

        return keyboard.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )