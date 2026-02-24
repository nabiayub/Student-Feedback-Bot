from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

from src.schemas.categories import CategoryBase
from src.schemas.users import UserBase

class AnnouncementCreate(BaseModel):
    telegram_id: int
    sent_users: int

    content: str

    user_id: int