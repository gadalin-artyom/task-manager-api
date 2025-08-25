import asyncio
import logging

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("DB Waiter")


async def wait_for_db() -> None:
    """Подключение к базе данных."""
    db_url = settings.database_url
    if not db_url:
        logger.error("Переменная окружения DATABASE_URL не установлена.")
        raise SystemExit(1)

    logger.info("Попытка подключиться к базе данных...")
    engine = create_async_engine(db_url)
    retries = 30
    retry_delay = 5

    for i in range(retries):
        try:
            async with engine.begin():
                logger.info("База данных готова к работе!")
                return
        except OperationalError as e:
            logger.warning(f"База данных ещё не готова: {e}")
            logger.info(
                f"Повторная попытка через {retry_delay} секунд... "
                f"(Попытка {i + 1}/{retries})",
            )
            await asyncio.sleep(retry_delay)

    logger.error(
        "Не удалось подключиться к базе данных после "
        "максимального количества попыток.",
    )
    raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(wait_for_db())
