from sqlalchemy import select, ScalarResult
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Admin


class AdminRepo():
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_admin(self, telegram_id: int) -> Admin:
        """
        Get admin by telegram_id
        :param telegram_id: int
        :return:
        """
        statement = select(Admin).where(Admin.telegram_id == telegram_id)
        admin = await self.__session.execute(statement)

        return admin.scalar_one_or_none()

    async def get_all_admin_id(self) -> ScalarResult[int]:
        """Get all admin id list"""
        statement = select(Admin.telegram_id)

        admins_ids = await self.__session.execute(statement)

        return admins_ids.scalars().all()

    async def create_new_admin(self, telegram_id: int) -> None:
        """Create new admin by telegram_id"""
        statement = (
            insert(Admin)
            .values(telegram_id=telegram_id)
            .on_conflict_do_nothing()
        )

        await self.__session.execute(statement)

        await self.__session.flush()

    async def delete_admin(self, telegram_id: int) -> None:
        """Delete admin by telegram_id"""
        admin = await self.get_admin(telegram_id)

        if admin:
            await self.__session.delete(admin)
            await self.__session.flush()