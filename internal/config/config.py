import os
from dotenv import load_dotenv

load_dotenv()


class ConfigError(Exception):
    """Ошибка конфигурации: не задана обязательная переменная окружения."""


class Config:
    APP_NAME = os.getenv("APP_NAME", "Online Testing Platform")
    APP_ENV = os.getenv("APP_ENV", "development")
    HTTP_PORT = int(os.getenv("HTTP_PORT", 8080))
    VERSION = os.getenv("VERSION", "1.0.0")
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")

    # --- PostgreSQL ---
    DB_HOST = os.getenv("DB_HOST", "")
    DB_PORT = os.getenv("DB_PORT") or "5432"
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "")
    DB_MAX_CONNS = 10  # заполняется в validate()

    def validate(self) -> None:
        """Проверяет обязательные переменные. Бросает ConfigError с понятным текстом."""
        for name in ("DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"):
            if not getattr(self, name):
                raise ConfigError(f"required environment variable {name} is not set")

        raw = os.getenv("DB_MAX_CONNS") or "10"
        try:
            max_conns = int(raw)
            if max_conns < 1:
                raise ValueError
        except ValueError:
            raise ConfigError("DB_MAX_CONNS must be a positive integer")
        self.DB_MAX_CONNS = max_conns


config = Config()