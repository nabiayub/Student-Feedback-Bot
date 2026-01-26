from typing import List
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cancel_name_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='Skip')

    keyboard.adjust(1)  # 1 button per row (important for size)

    return keyboard.as_markup(
        resize_keyboard=True,  # makes buttons compact
    )