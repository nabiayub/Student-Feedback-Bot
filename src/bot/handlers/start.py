from aiogram import Router, types

from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.repositories import CategoryRepo

router = Router()


@router.message(Command('start'))
async def start_bot(message: types.Message, session_without_commit: AsyncSession):
    category_repo = CategoryRepo(session=session_without_commit)
    categories = await category_repo.get_all_categories()

    text = f'''Hello {message.from_user.username} . Here is the list of all categories: \n'''

    for category in categories:
        text += category.title + '\n'

    await message.answer(text)
