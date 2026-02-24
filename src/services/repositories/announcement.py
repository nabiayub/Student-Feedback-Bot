from sqlite3 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.models import Announcement
from src.schemas.announcements import AnnouncementCreate


class AnnouncementRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create_announcement(self, announcement: AnnouncementCreate):
        print(announcement)
        db_announcement = Announcement(**announcement.model_dump())
        self.__session.add(db_announcement)

        try:
            await self.__session.flush()

        except IntegrityError:
            await self.__session.rollback()

