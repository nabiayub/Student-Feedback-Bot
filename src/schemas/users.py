from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """User base schema"""
    telegram_id: int
    username: str
    name: str | None = None

class UserCreate(UserBase):

    """User creation schema"""
    pass


class UserRead(UserBase):
    """User read schema"""
    id: int
    is_admin: bool = False
    registered: bool | None = False

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    """User update schema"""
    username: str | None = None
    name: str | None = None