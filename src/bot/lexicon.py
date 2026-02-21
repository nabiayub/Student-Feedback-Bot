from enum import Enum

class MainMenuButtons(str, Enum):
    WRITE_FEEDBACK = '✍️ Write feedback'
    PROFILE = '👤 Profile'
    ABOUT = 'ℹ️ About'


class GoBackButtons(str, Enum):
    BACK_TO_MENU = '⬅️ Back to Menu'
    GO_BACK = '⬅️ Go back'
    SKIP = '⏩ Skip'


class MessageButtons(str, Enum):
    FEEDBACK = 'Feedback'
    COMPLAINT = 'Complaint'
    SUGGESTION = 'Suggestion'

class ProfileButtons(str, Enum):
    CHANGE_NAME = '🖋 Change Name'
    SHOW_HISTORY = '📜 Show history'

class YesNoButtons(str, Enum):
    YES = 'Yes'
    NO = 'No'