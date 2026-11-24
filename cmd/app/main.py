import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from internal.config.config import config, ConfigError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")

# Проверка переменных окружения: при ошибке приложение не запускается
try:
    config.validate()
except ConfigError as e:
    print(f"[CONFIG] {e}", file=sys.stderr)
    sys.exit(1)
logging.getLogger("CONFIG").info("Environment variables loaded successfully")

from internal.database.postgres import db
from internal.controller import health_controller, auth_controller, test_controller


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()   # пул + повторные попытки; при неудаче приложение не стартует
    yield
    await db.close()


app = FastAPI(
    title=config.APP_NAME,
    version=config.VERSION,
    description="API для онлайн-платформы тестирования",
    lifespan=lifespan,
)

app.include_router(health_controller.router)
app.include_router(auth_controller.router)
app.include_router(test_controller.router)

if __name__ == "__main__":
    uvicorn.run("cmd.app.main:app", host="0.0.0.0", port=config.HTTP_PORT, reload=True)