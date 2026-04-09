from datetime import datetime
from sqlite3 import IntegrityError

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Message, User
from src.schemas.messages import MessageCreate, MessageRead


class MessageRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_messages_by_date_range(self, start_date: datetime, end_date: datetime) -> list[Message]:
        """
        Fetch all messages within a specific date range, joining with categories.
        """
        statement = (
            select(Message)
            .options(selectinload(Message.category))
            .where(Message.created_at.between(start_date, end_date))
            .order_by(Message.created_at.asc())
        )
        result = await self.__session.scalars(statement)
        return list(result.all())

    async def create_message_and_return_message(self, message: MessageCreate) -> Message:
        """Creates new message in database"""
        db_message = Message(**message.model_dump())
        self.__session.add(db_message)

        try:
            await self.__session.flush()
            return db_message

        except IntegrityError:
            await self.__session.rollback()





