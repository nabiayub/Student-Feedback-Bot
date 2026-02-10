from aiogram import Dispatcher, Router
from .start import router as start_router
from .profile import router as profile_router
from .message import router as message_router
from .about import router as about_router


def register_routers(dp: Dispatcher):
    user_router = Router()

    user_router.include_routers(
        start_router,
        profile_router,
        message_router,
        about_router
    )

    dp.include_router(user_router)
