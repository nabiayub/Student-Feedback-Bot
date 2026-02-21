from enum import Enum

class MainMenuButtons(str, Enum):
    WRITE_FEEDBACK = '✍️ Write feedback'
    PROFILE = '👤 Profile'
    ABOUT = 'ℹ️ About'


class GoBackButtons(str, Enum):
    BACK_TO_MENU = '⬅️ Back to Menu'
    GO_BACK = '⬅️ Go back'


class MessageButtons(str, Enum):
    FEEDBACK = 'Feedback'
    COMPLAINT = 'Complaint'
    SUGGESTION = 'Suggestion'