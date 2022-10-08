from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    """Конфиг тестов."""

    redis_host: str = Field('redis', env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    es_host: str = Field('elasticsearch', env="ELASTIC_HOST")
    es_port: int = Field(9200, env="ELASTIC_PORT")
    es_index: str = Field('movies', env="ES_INDEX")
    es_id_field: str = Field('id', env="ES_ID_FIELD")
    es_index_mapping: dict = Field({}, env="ES_INDEX_MAPPING")

    service_url: str = Field('http://nginx:80', env="SERVICE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


test_settings = TestSettings()
