from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas.users import UserRead, UserCreate



class UserRepository:
    """Class to manage all User table queries."""
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_user_by_telegram_id_or_none(self, telegram_id: int) -> UserRead | None:
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

        if not db_user:
            db_user = User(
                telegram_id=user.telegram_id,
                username=user.username
            )
            self.__session.add(db_user)
            await self.__session.flush()




















