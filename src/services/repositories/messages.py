from sqlite3 import IntegrityError

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Message, User
from src.schemas.messages import MessageCreate, MessageRead


class MessageRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_message_and_return_message(self, message: MessageCreate) -> Message:
        """Creates new message in database"""
        db_message = Message(**message.model_dump())
        self.__session.add(db_message)

        try:
            await self.__session.flush()
            return db_message

        except IntegrityError:
            await self.__session.rollback()





