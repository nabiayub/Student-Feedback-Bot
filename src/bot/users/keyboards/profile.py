from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class Profile:
    """
    Class for profile keyboards
    """
    @staticmethod
    def cancel_name_kb() -> ReplyKeyboardMarkup:
        """
        Cancels setting name reply button.
        :return: ReplyKeyboardMarkup instance
        """
        keyboard = ReplyKeyboardBuilder()
        keyboard.button(text='Skip')

        keyboard.adjust(1)  # 1 button per row (important for size)

        return keyboard.as_markup(
            resize_keyboard=True,
        )



