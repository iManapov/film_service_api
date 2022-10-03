import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field


logging_config.dictConfig(LOGGING)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    """Конфиг сервиса"""

    project_name: str = Field(..., env="PROJECT_NAME")

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")

    elastic_host: str = Field(..., env="ELASTIC_HOST")
    elastic_port: int = Field(..., env="ELASTIC_PORT")

    default_page_size: int = 50
    default_page_number: int = 1

    class Config:
        env_file = "core/.env"
        env_file_encoding = "utf-8"


settings = Settings()
