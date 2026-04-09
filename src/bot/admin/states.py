from aiogram.fsm.state import State, StatesGroup

class AnnouncementState(StatesGroup):
    ANNOUNCEMENT_TEXT = State()
    CONFIRM_ANNOUNCEMENT = State()

class ExportState(StatesGroup):
    CHOOSE_FORMAT = State()
    CHOOSE_RANGE = State()
    START_DATE = State()
    END_DATE = State()