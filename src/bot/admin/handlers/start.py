from aiogram import Router, F
from aiogram.types import Message

from src.bot.lexicon import MainMenuButtons

router = Router()

@router.message(F.text == MainMenuButtons.ADMIN_PANEL)
async def admin_panel(message: Message):
    await message.answer('Hello' + message.from_user.username)
