from typing import Optional, List

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base  # your created_at/updated_at mixin


class User(Base):
    """Users table"""
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, autoincrement=False)


    def __repr__(self):
        return f"<User: telegram_id={self.telegram_id}')>"
