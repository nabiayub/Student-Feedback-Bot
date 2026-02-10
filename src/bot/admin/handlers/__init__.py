from aiogram import Dispatcher, Router
from src.config.settings import settings


def register_routers(dp: Dispatcher):
  admin_router = Router()

  admin_router.message.filter(lambda message: message.from_user.id in settings.ADMIN_IDS)
  admin_router.callback_query.filter(lambda callback: callback.from_user.id in settings.ADMIN_IDS)

  admin_router.include_routers()

  dp.include_router(admin_router)