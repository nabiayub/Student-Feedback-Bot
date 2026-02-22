import logging
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from src.factory import create_bot, create_dispatcher
from src.bot.router import register_all_routers
from src.bot.middlewares import register_middlewares
from src.config.settings import settings


async def on_startup(bot):
    # Set up Admin-specific menu
    # Set Webhook URLx`
    await bot.set_webhook(f"{settings.BASE_URL}{settings.WEBHOOK_PATH}", drop_pending_updates=True)


async def on_shutdown(bot):
    await bot.delete_webhook()
    await bot.session.close()


def main():
    logging.basicConfig(level=logging.INFO)

    bot = create_bot()
    dp = create_dispatcher()

    # Manual registration as requested
    register_middlewares(dp)
    register_all_routers(dp)

    # Lifecycle hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    main()