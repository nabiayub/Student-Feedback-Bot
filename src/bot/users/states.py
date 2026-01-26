from aiogram.fsm.state import State, StatesGroup


class UserNameState(StatesGroup):
    NAME= State()
    CONFIRM_NAME = State()

