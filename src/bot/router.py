from aiogram import Router, Dispatcher
from .admin.handlers import register_routers as admin_register_routers
from .users.handlers import register_routers as users_register_routers

def register_all_routers(dp: Dispatcher):
    admin_register_routers(dp)
    users_register_routers(dp)
