from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from src.database.models import Category

class CategoryRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_all_categories(self) -> ScalarResult[Category]:
        """
        Fetch all categories
        :return: ScalarResult[Category]
        """
        statement = select(Category)

        return await self.__session.scalars(statement)







