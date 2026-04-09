from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from src.database.db import async_session_maker


class SessionProxy:
    """
    A proxy for the database session that initializes only when accessed.
    """
    def __init__(self, session_maker):
        self._session_maker = session_maker
        self._session = None

    def get_session(self):
        if self._session is None:
            self._session = self._session_maker()
        return self._session

    def __getattr__(self, name):
        return getattr(self.get_session(), name)

    async def commit(self):
        if self._session:
            await self._session.commit()

    async def rollback(self):
        if self._session:
            await self._session.rollback()

    async def close(self):
        if self._session:
            await self._session.close()
            self._session = None


class BaseDatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        proxy = SessionProxy(async_session_maker)
        self.set_session(data, proxy)
        try:
            result = await handler(event, data)
            await self.after_handler(proxy)
            return result
        except Exception as e:
            await proxy.rollback()
            raise e
        finally:
            await proxy.close()


    def set_session(self, data: Dict[str, Any], session: SessionProxy) -> None:
        """
        A method for setting (assigning) a session to the data. Implemented in child classes.
        :param data:
        :param session:
        :return:
        """
        raise NotImplementedError("Этот метод должен быть реализован в подклассах.")

    async def after_handler(self, session: SessionProxy) -> None:
        """
        Method for executing tasks after handling query. By default, does nothing.
        :param session: Database Session by sessionmaker.
        :return:
        """
        pass



class DatabaseMiddlewareWithCommit(BaseDatabaseMiddleware):
    def set_session(self, data: Dict[str, Any], session: SessionProxy) -> None:
        """Set session with commit"""
        data['session_with_commit'] = session


    async def after_handler(self, session: SessionProxy) -> None:
        """Commit the session after handler"""
        await session.commit()


class DatabaseMiddlewareWithoutCommit(BaseDatabaseMiddleware):
    def set_session(self, data: Dict[str, Any], session: SessionProxy) -> None:
        """Set session without commit"""
        data['session_without_commit'] = session




