from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    telegram_id: int
    username: str
    name: Optional[str] = None

class UserRead(UserBase):
    id: int
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True