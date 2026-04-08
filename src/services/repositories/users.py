from sqlite3 import IntegrityError
from xml.dom.domreg import registered

from sqlalchemy import select, ScalarResult, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, Message
from src.schemas.messages import MessageRead
from src.schemas.users import UserCreate


class UserRepository:
    """Class to manage all User table queries."""

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_all_users_telegram_id(self) -> ScalarResult[int]:
        return await self.__session.scalars(select(User.telegram_id))

    async def get_user_by_telegram_id_or_none(self, telegram_id: int) -> User | None:
        """
        Get user by telegram id or none
        :param telegram_id:
        :return:
        """
        statement = select(User).where(User.telegram_id == telegram_id)
        result = await self.__session.execute(statement)
        db_user = result.scalar_one_or_none()

        return db_user

    async def get_or_create_user(self, user: UserCreate):
        """
        Get user by telegram_id or create new one.
        :param user: instance of UserBase schema
        :return: instance of UserRead schema
        """

        db_user = await self.get_user_by_telegram_id_or_none(user.telegram_id)

        if db_user:
            return db_user

        db_user = User(**user.model_dump())
        self.__session.add(db_user)

        try:
            await self.__session.flush()

        except IntegrityError:
            await self.__session.rollback()

            return db_user

        return db_user









