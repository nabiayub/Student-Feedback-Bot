from typing import Optional, List

from sqlalchemy import BigInteger, Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base  # your created_at/updated_at mixin


class User(Base):
    """Users table"""
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    username: Mapped[str | None]
    name: Mapped[Optional[str | None]] = mapped_column(String, nullable=True)

    # indicates that the user has been asked to write his name at registration.
    # No need to ask automatically after if he doesn't want to.
    registered = Mapped[bool] = mapped_column(Boolean, default=False)

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    messages: Mapped[List["Message"] | None] = relationship(
        "Message",
        back_populates="user",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<User(username='{self.username}, id={self.id}, telegram_id={self.telegram_id}')>"

