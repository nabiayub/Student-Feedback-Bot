from aiogram import Dispatcher

from src.middlewares.database import (
    DatabaseMiddlewareWithCommit,
    DatabaseMiddlewareWithoutCommit
)


def register_middlewares(dp: Dispatcher) -> None:
    '''
    Registers all middlewares for the dispatcher.

    :param dp: Aiogram Dispatcher instance
    '''
    dp.update.middleware(DatabaseMiddlewareWithCommit)
    dp.update.middleware(DatabaseMiddlewareWithoutCommit)

