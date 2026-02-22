from typing import List

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base

class Admin(Base):
    __tablename__ = 'admins'

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<Admin(telegram_id={self.telegram_id}, added_at={self.created_at})>"