from sqlite3 import IntegrityError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas.users import UserRead, UserCreate


class UserRepository:
    """Class to manage all User table queries."""

    def __init__(self, session: AsyncSession):
        self.__session = session

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
        :return: instqnce of UserRead schema
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

    async def set_name_and_registered_for_user(
            self,
            telegram_id: int,
            name: str = None
    ) -> None:
        """
        Method to set name of the user is User table.
        If method receives name, changes "name" and "registered" fields.
        Otherwise, name is set to none and only "registered" is set to True.
        :param telegram_id: Telegram ID
        :param name: Enter name. Default is None
        :return:
        """
        user: User = await self.get_user_by_telegram_id_or_none(telegram_id)

        if not user:
            return

        if name:
            user.name = name

        user.registered = True
