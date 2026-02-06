from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

from src.schemas.categories import CategoryBase


class MessageBase(BaseModel):
    content: str
    category_id: int
    is_anonymous: bool


class MessageCreate(MessageBase):
    user_id: int

class MessageRead(BaseModel):
    created_at: datetime

    content: str
    category: CategoryBase

    model_config = ConfigDict(from_attributes=True)

