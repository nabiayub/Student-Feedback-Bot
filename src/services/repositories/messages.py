from sqlite3 import IntegrityError

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Message, User
from src.schemas.messages import MessageCreate, MessageRead


class MessageRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_message(self, message: MessageCreate) -> None:
        """Creates new message in database"""
        db_message = Message(**message.model_dump())
        self.__session.add(db_message)

        try:
            await self.__session.flush()

        except IntegrityError:
            await self.__session.rollback()

    async def get_messages_of_one_user(
            self,
            telegram_id: int,
            page: int,
            limit: int = 5
    ) -> tuple[list[MessageRead] | None, bool] :
        """Returns messages of user's by telegram id."""
        offset = (page - 1) * limit

        statement = (
            select(Message)
            .join(User)
            .where(User.telegram_id == telegram_id)
            .options(selectinload(Message.category))
            .order_by(Message.created_at.desc())
            .limit(limit + 1)
            .offset(offset)
        )

        result = await self.__session.execute(statement)
        messages = result.scalars().all()

        has_next = len(messages) > limit

        messages = messages[:limit]

        return [MessageRead.model_validate(msg) for msg in messages], has_next
