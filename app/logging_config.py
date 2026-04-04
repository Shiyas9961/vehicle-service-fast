import logging
from logging.config import dictConfig
from pathlib import Path

from app.config import settings


def configure_logging() -> Path:
    log_dir = Path(settings.LOG_DIR)
    if not log_dir.is_absolute():
        log_dir = Path(__file__).resolve().parent.parent / log_dir
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / settings.LOG_FILE
    log_level = settings.LOG_LEVEL.upper()

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "standard",
                    "level": log_level,
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(log_file),
                    "maxBytes": settings.LOG_MAX_BYTES,
                    "backupCount": settings.LOG_BACKUP_COUNT,
                    "encoding": "utf-8",
                    "formatter": "standard",
                    "level": log_level,
                },
            },
            "root": {
                "handlers": ["console", "file"],
                "level": log_level,
            },
            "loggers": {
                "uvicorn": {
                    "handlers": ["console", "file"],
                    "level": log_level,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["console", "file"],
                    "level": log_level,
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["console", "file"],
                    "level": log_level,
                    "propagate": False,
                },
            },
        }
    )

    logging.captureWarnings(True)
    logging.getLogger("app.logging").info("Logging configured. File output: %s", log_file.resolve())

    return log_file
