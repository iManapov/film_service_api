from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Конфиг тестов"""

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")

    elastic_host: str = Field(..., env="ELASTIC_HOST")
    elastic_port: int = Field(..., env="ELASTIC_PORT")

    class Config:
        env_file = "tests/.env"
        env_file_encoding = "utf-8"


settings = Settings()