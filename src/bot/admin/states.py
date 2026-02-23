from aiogram.fsm.state import State, StatesGroup

class AnnouncementState(StatesGroup):
    ANNOUNCEMENT_TEXT = State()
    CONFIRM_ANNOUNCEMENT = State()