from src.config.settings import settings
from src.services.repositories.admins import AdminRepo


class AdminManager:
    """Class for managing admins"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AdminManager, cls).__new__(cls)

            cls._instance._admins = set()
            cls._instance._is_initialized = False

        return cls._instance

    async def is_admin(self, telegram_id: int) -> bool:
        """Checks whether user is admin by telegram_id"""
        return telegram_id in self._admins

    async def get_all_admins(self) -> set[int]:
        return self._admins

    async def update_admins_list(self, session_without_commit):
        """Update admins list"""
        admin_repo = AdminRepo(session_without_commit)

        new_admins = set(settings.ADMIN_IDS)

        db_admins = await admin_repo.get_all_admin_id()
        new_admins.update(db_admins)

        self._admins = new_admins
        self._is_initialized = True

admin_manager = AdminManager()
