from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.bot.lexicon import AdminExportButtons, GoBackButtons

def export_format_kb() -> InlineKeyboardMarkup:
    """Keyboard for selecting export format"""
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=AdminExportButtons.EXCEL.value, callback_data="export_excel")
    keyboard.button(text=AdminExportButtons.CSV.value, callback_data="export_csv")
    keyboard.button(text=GoBackButtons.RETURN_TO_ADMIN_PANEL.value, callback_data="back_to_admin")

    keyboard.adjust(2, 1)

    return keyboard.as_markup()

def export_range_kb() -> InlineKeyboardMarkup:
    """Keyboard for selecting export range"""
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=AdminExportButtons.EXPORT_ALL.value, callback_data="range_all")
    keyboard.button(text=AdminExportButtons.CUSTOM_RANGE.value, callback_data="range_custom")
    keyboard.button(text=GoBackButtons.GO_BACK.value, callback_data="range_back")

    keyboard.adjust(2, 1)

    return keyboard.as_markup()
