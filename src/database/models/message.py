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

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey('categories.id', ondelete="SET NULL"),
        nullable=True
    )

    admin_group_message_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, nullable=True)

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="messages",
    )

    def __repr__(self):
        return f"<Message category='{self.category.title}'>"
