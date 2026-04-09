from sqlite3 import IntegrityError
from xml.dom.domreg import registered

from sqlalchemy import select, ScalarResult, func
from sqlalchemy.dialects.postgresql import insert
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

    async def register_user(self, telegram_id: int):
        """
        Register user by telegram id.
        """

        try:
            statement = insert(User).values(telegram_id=telegram_id)
            statement = statement.on_conflict_do_nothing(index_elements=['telegram_id'])

            await self.__session.execute(statement)

        except IntegrityError:
            await self.__session.rollback()









