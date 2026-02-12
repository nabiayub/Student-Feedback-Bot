from typing import List

from aiohttp.abc import StreamResponse
from sqlalchemy import BigInteger, Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import User, Category
from src.database.models.base import Base


class Message(Base):
    """
    Message table
    """
    __tablename__ = 'messages'

    content: Mapped[str] = mapped_column(String)
    is_anonymous: Mapped[bool] = mapped_column(Boolean)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id', ondelete="SET NULL"),
        nullable=True
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey('categories.id', ondelete="SET NULL"),
        nullable=True
    )

    admin_group_message_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="messages",
    )
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="messages",
    )

    def __repr__(self):
        username = self.user.username if self.user else None
        telegram_id = self.user.telegram_id if self.user else None
        return f"<Message user={username} telegram_id={telegram_id}>"
