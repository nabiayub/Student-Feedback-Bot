from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

class HistoryPaginatorCBData(CallbackData, prefix='history'):
    page: int
    action: str # "previous, next, ignore"


def cancel_name_kb() -> ReplyKeyboardMarkup:
    """
    Cancels setting name reply button.
    :return: ReplyKeyboardMarkup instance
    """
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='⏩ Skip')

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True)

def profile_kb() -> ReplyKeyboardMarkup:
    """Keyboard for profile reply buttons: Change name and view history"""
    keyboard = ReplyKeyboardBuilder()

    keyboard.button(text='🖋 Change Name')
    keyboard.button(text='📜 Show history')
    keyboard.button(text='⬅️ Back to Menu')

    keyboard.adjust(2, 1)

    return keyboard.as_markup(resize_keyboard=True)

def get_history_paginator_cb(page: int, has_next: bool) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    if page > 1:
        keyboard.button(
            text='⬅️',
            callback_data=HistoryPaginatorCBData(page=page - 1, action='previous')
        )
    keyboard.button(
        text=f'{page}',
        callback_data=HistoryPaginatorCBData(page=page - 1, action='ignore')
    )

    if has_next:
        keyboard.button(
            text='➡️️',
            callback_data=HistoryPaginatorCBData(page=page + 1, action='next')
        )

    keyboard.adjust(3)
    return keyboard.as_markup()