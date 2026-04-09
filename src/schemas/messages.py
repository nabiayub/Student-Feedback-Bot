from wsgiref.simple_server import make_server

from pydantic import BaseModel, ConfigDict
from datetime import datetime

from src.schemas.categories import CategoryBase


class MessageBase(BaseModel):
    content: str
    category_id: int


class MessageCreate(MessageBase):
    pass


class MessageRead(BaseModel):
    created_at: datetime

    content: str
    category: CategoryBase

    model_config = ConfigDict(from_attributes=True)


class MessageForTelegramGroup(BaseModel):
    message_id: int

    content: str
    category_title: str

    def create_text_for_telegram_message(self):
        text = (
            # f'№{self.id} - {self.category_title} - {sender}\n'
            f'{self.content}\n\n'
            f'№ {self.message_id} - {self.category_title}\n'

        )

        return text
