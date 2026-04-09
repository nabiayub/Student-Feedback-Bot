
from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base


class Announcement(Base):
    __tablename__ = 'announcements'

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True)

    content: Mapped[str] = mapped_column(String)

    sent_users: Mapped[int] = mapped_column(Integer, default=0)


    def __repr__(self):
        return f'<Announcement(admin={self.telegram_id}>'