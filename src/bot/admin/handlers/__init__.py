from aiogram import Dispatcher, Router

from src.config.settings import settings
from src.bot.admin.handlers.start import router as start_router
from src.bot.admin.handlers.post_announcement import router as post_announcement_router

from ...filters.admin import IsAdminFilter


def register_routers(dp: Dispatcher):
    admin_router = Router()

    # uncomment when going to production
    # admin_router.message.filter(IsAdminFilter())
    # admin_router.callback_query.filter(IsAdminFilter())

    admin_router.message.filter(lambda message: message.from_user.id in settings.ADMIN_IDS)
    admin_router.callback_query.filter(lambda message: message.from_user.id in settings.ADMIN_IDS)

    admin_router.include_routers(
        start_router,
        post_announcement_router
    )

    dp.include_router(admin_router)
