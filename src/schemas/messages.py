from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

from src.schemas.categories import CategoryRead
from src.schemas.users import UserRead


class MessageBase(BaseModel):
    content: str
    category_id: int
    is_anonymous: bool


class MessageCreate(MessageBase):
    user_id: int

class MessageRead(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    user: UserRead
    category: CategoryRead

    model_config = ConfigDict(from_attributes=True)

