from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from src.bot.admin.keyboards.export_kb import export_format_kb, export_range_kb
from src.bot.admin.states import ExportState
from src.bot.lexicon import AdminMenuButtons
from src.bot.admin.handlers.start import admin_panel
from src.services.repositories.messages import MessageRepo
from src.bot.admin.services.exporter import ExportService
from datetime import datetime
from typing import Any
import os

router = Router()

async def _perform_export(callback: types.CallbackQuery, state: FSMContext, session: Any, start_date: datetime, end_date: datetime):
    """
    Helper to perform the actual export and send the file.
    """
    data = await state.get_data()
    format_type = data.get('format')

    await callback.message.edit_text("⏳ <b>Generating report...</b> Please wait.")
    
    # 1. Fetch data from DB
    repo = MessageRepo(session)
    messages = await repo.get_messages_by_date_range(start_date, end_date)
    
    if not messages:
        await callback.message.answer("❌ No messages found for the selected period.")
        await state.clear()
        await admin_panel(callback.message, state)
        return

    # 2. Generate file
    filename = f"feedbacks_{start_date.strftime('%d_%m_%Y')}"
    if format_type == "Excel":
        file_path = f"{filename}.xlsx"
        ExportService.generate_excel(messages, file_path)
    else:
        file_path = f"{filename}.csv"
        ExportService.generate_csv(messages, file_path)

    # 3. Send file
    await callback.message.answer_document(
        FSInputFile(file_path),
        caption=f"📊 Feedback Report\n📅 Period: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}"
    )
    
    # 4. Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)
        
    await state.clear()
    await admin_panel(callback.message, state)

@router.message(F.text == AdminMenuButtons.EXPORT_DATA)
async def start_export(message: types.Message, state: FSMContext):
    """
    Initial step of export: Choose format.
    """
    # Remove the reply keyboard first
    await message.answer(
        text="🔄 Loading export options...",
        reply_markup=types.ReplyKeyboardRemove()
    )
    
    # Send the inline keyboard for format selection
    await message.answer(
        "📊 <b>Export Data</b>\n\nPlease select the file format you'd like to receive:",
        reply_markup=export_format_kb(),
    )
    await state.set_state(ExportState.CHOOSE_FORMAT)

@router.callback_query(ExportState.CHOOSE_FORMAT, F.data.in_({"export_excel", "export_csv"}))
async def choose_range_menu(callback: types.CallbackQuery, state: FSMContext):
    """
    Format selected -> Ask for range (All / Custom).
    """
    format_type = "Excel" if callback.data == "export_excel" else "CSV"
    await state.update_data(format=format_type)
    
    await callback.message.edit_text(
        f"📄 Format: <b>{format_type}</b>\n\nSelect the time period for your report:",
        reply_markup=export_range_kb()
    )
    await state.set_state(ExportState.CHOOSE_RANGE)

@router.callback_query(ExportState.CHOOSE_RANGE, F.data == "range_all")
async def export_all_time(callback: types.CallbackQuery, state: FSMContext, session_without_commit: Any):
    """
    Export all messages from 1970 to now.
    """
    start_date = datetime(1970, 1, 1)
    end_date = datetime.now()
    await _perform_export(callback, state, session_without_commit, start_date, end_date)
    await callback.answer()

@router.callback_query(ExportState.CHOOSE_RANGE, F.data == "range_custom")
async def start_custom_range(callback: types.CallbackQuery, state: FSMContext):
    """
    Start the calendar flow.
    """
    await callback.message.edit_text(
        "📅 <b>Select Start Date</b>\n\nPlease pick the beginning of the period:",
        reply_markup=await SimpleCalendar().start_calendar()
    )
    await state.set_state(ExportState.START_DATE)

@router.callback_query(ExportState.CHOOSE_RANGE, F.data == "range_back")
async def back_to_format(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📊 <b>Export Data</b>\n\nPlease select the file format you'd like to receive:",
        reply_markup=export_format_kb(),
    )
    await state.set_state(ExportState.CHOOSE_FORMAT)
    await callback.answer()

@router.callback_query(ExportState.START_DATE, SimpleCalendarCallback.filter())
async def process_start_date(callback: types.CallbackQuery, callback_data: SimpleCalendarCallback, state: FSMContext):
    """
    Processes Start Date and asks for End Date.
    """
    if callback_data.act == "CANCEL":
        await state.clear()
        await callback.answer("Export canceled")
        await callback.message.delete()
        await admin_panel(callback.message, state)
        return

    selected, date = await SimpleCalendar().process_selection(callback, callback_data)
    if selected:
        await state.update_data(start_date=date)
        
        await callback.message.edit_text(
            f"✅ Start Date: {date.strftime('%d.%m.%Y')}\n"
            "📅 <b>Step 2: Select End Date</b>\n\nPlease pick the end of the period:",
            reply_markup=await SimpleCalendar().start_calendar()
        )
        await state.set_state(ExportState.END_DATE)
    await callback.answer()

@router.callback_query(ExportState.END_DATE, SimpleCalendarCallback.filter())
async def process_end_date(callback: types.CallbackQuery, callback_data: SimpleCalendarCallback, state: FSMContext, session_without_commit):
    """
    Processes End Date, generates file and sends it.
    """
    if callback_data.act == "CANCEL":
        await state.clear()
        await callback.answer("Export canceled")
        await callback.message.delete()
        await admin_panel(callback.message, state)
        return

    selected, end_date = await SimpleCalendar().process_selection(callback, callback_data)
    if selected:
        data = await state.get_data()
        start_date = data.get('start_date')
        
        # Ensure correct chronological order
        if end_date < start_date:
            start_date, end_date = end_date, start_date
        
        await _perform_export(callback, state, session_without_commit, start_date, end_date)
    await callback.answer()


@router.callback_query(ExportState.CHOOSE_FORMAT, F.data == "back_to_admin")
async def back_to_admin(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.delete()
    await admin_panel(callback.message, state)
