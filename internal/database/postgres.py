import asyncio
import logging

from psycopg.conninfo import make_conninfo
from psycopg_pool import AsyncConnectionPool

from internal.config.config import config

logger = logging.getLogger("DATABASE")

MAX_ATTEMPTS = 10


class Database:
    """Пул соединений с PostgreSQL (ограниченный размер, повторные попытки при старте)."""

    def __init__(self) -> None:
        self.pool: AsyncConnectionPool | None = None

    async def connect(self) -> None:
        # make_conninfo сам экранирует спецсимволы в пароле
        conninfo = make_conninfo(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            connect_timeout=3,
        )

        last_error: Exception | None = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            pool = AsyncConnectionPool(
                conninfo,
                min_size=min(2, config.DB_MAX_CONNS),
                max_size=config.DB_MAX_CONNS,
                max_lifetime=30 * 60,
                max_idle=5 * 60,
                check=AsyncConnectionPool.check_connection,
                open=False,
            )
            try:
                await pool.open()
                await pool.wait(timeout=5)  # реально ждём готовых соединений
                self.pool = pool
                logger.info(
                    "Successfully connected to PostgreSQL at %s:%s",
                    config.DB_HOST, config.DB_PORT,
                )
                return
            except Exception as e:
                last_error = e
                await pool.close()
                wait = attempt  # линейно растущая пауза
                logger.warning(
                    "attempt %d/%d failed: %s; retry in %ds",
                    attempt, MAX_ATTEMPTS, e, wait,
                )
                await asyncio.sleep(wait)

        raise RuntimeError(
            f"database is unavailable after {MAX_ATTEMPTS} attempts: {last_error}"
        )

    async def ping(self, timeout: float = 2.0) -> bool:
        """True, если БД отвечает на SELECT 1."""
        if self.pool is None:
            return False
        try:
            async with asyncio.timeout(timeout):
                async with self.pool.connection() as conn:
                    await conn.execute("SELECT 1")
            return True
        except Exception:
            return False

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()


db = Database()