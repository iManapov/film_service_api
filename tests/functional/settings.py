from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    """Конфиг тестов"""

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")

    elastic_host: str = Field(..., env="ELASTIC_HOST")
    elastic_port: int = Field(..., env="ELASTIC_PORT")
    elastic_movies_index: str = Field(..., env="ELASTIC_MOVIES_INDEX")
    elastic_genres_index: str = Field(..., env="ELASTIC_GENRES_INDEX")
    elastic_persons_index: str = Field(..., env="ELASTIC_PERSONS_INDEX")
    elastic_id_field: str = 'id'
    # elastic_index_mapping: dict =

    service_url: str = Field(..., env="FAST_API_URL")

    class Config:
        env_file = "tests/.env"
        env_file_encoding = "utf-8"


test_settings = TestSettings()