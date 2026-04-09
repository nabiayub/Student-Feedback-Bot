from enum import Enum

class MainMenuButtons(str, Enum):
    WRITE_FEEDBACK = '✍️ Write feedback'
    PROFILE = '👤 Profile'
    ABOUT = 'ℹ️ About'
    ADMIN_PANEL = '🛠 Admin Panel'


class GoBackButtons(str, Enum):
    BACK_TO_MENU = '⬅️ Back to Menu'
    GO_BACK = '⬅️ Go back'
    SKIP = '⏩ Skip'
    RETURN_TO_ADMIN_PANEL = '⬅️ Admin Panel'

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

class AdminMenuButtons(str, Enum):
    POST_ANNOUNCEMENT = '🔔 Announcement'
    ANALYTICS = '📊 Analytics'
    EXPORT_DATA = '📥 Export Data'

class AdminExportButtons(str, Enum):
    EXCEL = '📊 Excel (.xlsx)'
    CSV = '📄 CSV (.csv)'

class AdminAnnouncementButtons(str, Enum):
    CONFIRM_ANNOUNCEMENT = '✅ Send'
    CANCEL_ANNOUNCEMENT = '❌ Cancel'
    GO_BACK = '⬅️ Go back'


