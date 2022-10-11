from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    """Конфиг тестов"""

    redis_host: str = Field("redis", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    elastic_host: str = Field("elasticsearch", env="ELASTIC_HOST")
    elastic_port: int = Field(9200, env="ELASTIC_PORT")
    elastic_movies_index: str = Field("movies", env="ELASTIC_MOVIES_INDEX")
    elastic_genres_index: str = Field("genres", env="ELASTIC_GENRES_INDEX")
    elastic_persons_index: str = Field("persons", env="ELASTIC_PERSONS_INDEX")
    elastic_id_field: str = "id"

    service_url: str = Field("http://nginx:80", env="FAST_API_URL")

    class Config:
        env_file = "tests/functional/.env"
        env_file_encoding = "utf-8"


test_settings = TestSettings()
