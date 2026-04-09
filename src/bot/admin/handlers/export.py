from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from src.bot.admin.keyboards.export_kb import export_format_kb
from src.bot.admin.states import ExportState
from src.bot.lexicon import AdminMenuButtons, AdminExportButtons, GoBackButtons
from src.bot.admin.handlers.start import admin_panel

router = Router()

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
async def choose_range(callback: types.CallbackQuery, state: FSMContext):
    """
    Next step: Inform about the calendar (Step 4 will implement this).
    """
    format_type = "Excel" if callback.data == "export_excel" else "CSV"
    await state.update_data(format=format_type)
    
    # This is a placeholder until Step 4 (Calendar Integration)
    await callback.message.edit_text(
        f"Format selected: {format_type}\n\n"
        "Step 4 will integrate the Calendar here for date selection.\n"
        "For now, Step 3 is focused on the FSM and Menu structure."
    )
    # We'll go back to admin panel for now to allow verification of Step 3
    await state.clear()
    await callback.answer()
    await admin_panel(callback.message, state)

@router.callback_query(ExportState.CHOOSE_FORMAT, F.data == "back_to_admin")
async def back_to_admin(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.delete()
    await admin_panel(callback.message, state)
