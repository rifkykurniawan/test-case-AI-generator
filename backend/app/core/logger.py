import sys

from loguru import logger

from app.core.config import settings


def configure_logging() -> None:
    """Configure loguru logging based on app settings."""
    logger.remove()

    # Custom format containing timestamp, log level, and message details
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL.upper(),
        format=log_format,
        colorize=True,
    )

    logger.info("Logging configured. Level: {}", settings.LOG_LEVEL)
