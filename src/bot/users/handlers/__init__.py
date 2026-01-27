from aiogram import Dispatcher
from .start import router as start_router
from src.bot.users.handlers.profile import router as profile_router

def register_routers(dp: Dispatcher):
  dp.include_router(start_router)
  dp.include_router(profile_router)