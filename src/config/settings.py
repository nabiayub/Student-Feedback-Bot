import os
from typing import List
from loguru import logger as loguru_logger

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Bot settings loaded from .env using Pydantic Settings.
    """
    BOT_TOKEN: str
    ADMIN_ID: List[int]
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def configure_logger(self):
        """
        Configure the Loguru logger for the bot.

        - Logs are written to a file with rotation.
        - Format, rotation size, retention, and compression are configurable.
        - Removes default console handler to avoid duplicate logs.

        Returns:
            loguru.logger: Configured logger instance.
        """
        loguru_logger.remove()  # remove default handler
        loguru_logger.add(
            "logs/bot.log",
            rotation=self.LOG_ROTATION,
            format=self.FORMAT_LOG,
            level="INFO",
            retention="7 days",
            compression="zip",
        )
        return loguru_logger


settings = Settings()
logger = settings.configure_logger()