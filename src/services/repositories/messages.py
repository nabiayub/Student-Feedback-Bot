from sqlite3 import IntegrityError

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Message
from src.schemas.messages import MessageCreate


class MessageRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_message(self, message: MessageCreate) -> None:
        db_message = Message(**message.model_dump())
        self.__session.add(db_message)

        try:
            await self.__session.flush()

        except IntegrityError as e:
            await self.__session.rollback()

