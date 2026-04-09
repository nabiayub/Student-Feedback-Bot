from src.config.settings import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


if settings.IS_PRODUCTION:
    # Production settings (Frankfurt Bot ↔ Frankfurt DB)
    engine_params = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 10,
        "max_overflow": 20
    }
else:
    # Local Dev settings (Tashkent Bot ↔ Frankfurt DB)
    # We remove the ping to get our speed back!
    engine_params = {
        "pool_pre_ping": True,
        "pool_recycle": 60,  # Frequent refresh to avoid timeouts
        "pool_size": 5,
        "max_overflow": 5
    }

engine = create_async_engine(
    settings.DATABASE_URL,
    **engine_params
)

# Создание фабрики сессий
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)
