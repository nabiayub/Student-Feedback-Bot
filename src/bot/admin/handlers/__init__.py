from aiogram import Dispatcher, Router

from ..handlers.start import router as start_router


def register_routers(dp: Dispatcher):
  admin_router = Router()


  admin_router.include_routers(
      start_router,
  )

  dp.include_router(admin_router)