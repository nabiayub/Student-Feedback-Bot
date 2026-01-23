from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from src.database.db import async_session_maker


class BaseDatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        async with async_session_maker() as session:
            self.set_session(data, session)  # Устанавливаем сессию
            try:
                result = await handler(event, data)
                await self.after_handler(session)
                return result
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    def set_session(self, data: Dict[str, Any], session) -> None:
        """
        A method for setting (assigning) a session to the data. Implemented in child classes.
        :param data:
        :param session:
        :return:
        """
        raise NotImplementedError("Этот метод должен быть реализован в подклассах.")

    async def after_handler(self, session) -> None:
        """
        Method for executing tasks after handling query. By default, does nothing.
        :param session: Database Session by sessionmaker.
        :return:
        """
        pass



class DatabaseMiddlewareWithCommit(BaseDatabaseMiddleware):
    def set_session(self, data: Dict[str, Any], session) -> None:
        """Set session with commit"""
        data['session_with_commit'] = session


    async def after_handler(self, session) -> None:
        """Commit the session after handler"""
        await session.commit()


class DatabaseMiddlewareWithoutCommit(BaseDatabaseMiddleware):
    def set_session(self, data: Dict[str, Any], session) -> None:
        """Set session without commit"""
        print(session)
        data['session_without_commit'] = session




