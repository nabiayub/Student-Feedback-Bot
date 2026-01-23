from src.config.settings import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


# Создание асинхронного движка для подключения к БД
engine = create_async_engine(url=settings.DATABASE_URL)

# Создание фабрики сессий
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)