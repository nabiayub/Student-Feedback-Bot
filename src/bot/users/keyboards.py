from typing import List
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def cancel_name_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Skip', callback_data='skip_name')

    keyboard.adjust(1)  # 1 button per row (important for size)

    return keyboard.as_markup(
        resize_keyboard=True,  # makes buttons compact
        one_time_keyboard=True  # optional: hides after press
    )