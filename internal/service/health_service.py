import time
from internal.config.config import config
from internal.database.postgres import db

START_TIME = time.time()


class HealthService:
    @staticmethod
    async def get_health_status():
        db_ok = await db.ping()
        uptime = time.time() - START_TIME
        return {
            "status": "pass" if db_ok else "fail",
            "db": "up" if db_ok else "down",
            "app_name": config.APP_NAME,
            "version": config.VERSION,
            "environment": config.APP_ENV,
            "uptime": f"{uptime:.2f} seconds",
        }