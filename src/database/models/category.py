from typing import Optional, List

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base

class Category(Base):
    __tablename__ = 'categories'

    title: Mapped[str] = mapped_column(String(100))

    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
        passive_deletes=True
    )

    def __repr__(self):
        return f'<Category {self.title}>'



