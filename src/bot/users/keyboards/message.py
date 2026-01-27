from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class MessageKeyboard:
    @staticmethod
    def ask_anonymous_kb() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardBuilder()

        keyboard.button(text='Yes')
        keyboard.button(text='No')

        keyboard.adjust(2)

        return keyboard.as_markup(
            resize_keyboard=True,
        )

    @staticmethod
    def confirm_or_skip_message_kb() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardBuilder()

        keyboard.button(text='Confirm')
        keyboard.button(text='Cancel')

        keyboard.adjust(2)

        return keyboard.as_markup(
            resize_keyboard=True,
        )
