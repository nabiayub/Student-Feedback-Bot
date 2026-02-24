
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Base


class Announcement(Base):
    __tablename__ = 'announcements'

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id', ondelete="SET NULL"),
        nullable=True
    )

    content: Mapped[str] = mapped_column(String)

    sent_users: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="announcements",
    )

    def __repr__(self):
        return f'<Announcement(admin={self.user_id}, content={self.content})>'