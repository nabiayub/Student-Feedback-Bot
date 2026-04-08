from aiogram.fsm.state import State, StatesGroup


class MessageState(StatesGroup):
    CATEGORY_ID = State()
    CONTENT = State()
    CONFIRM_MESSAGE = State()

