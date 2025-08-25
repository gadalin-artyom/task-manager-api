import logging
import sys

from app.core.config import BASE_DIR, settings

LOG_DIR = BASE_DIR / settings.log_path
LOG_DIR.mkdir(exist_ok=True, parents=True)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "{asctime}   {levelname}:   {name} | {module} | {message}"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "app.log"),
            "formatter": "verbose",
            "encoding": "utf-8",
            "level": "INFO",
            "maxBytes": 3_145_728,
            "backupCount": 3,
        },
    },
    "loggers": {
        "app": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
