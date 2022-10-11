# Код функциональных тестов

## Локальный запуск
Для запуска тестов локально необходимо создать файл `tests/functional/.env` со следующими параметрами:

- REDIS_HOST - хост redis
- REDIS_PORT - порт redis
- ELASTIC_HOST - хост Elasticsearch
- ELASTIC_PORT - порт Elasticsearch
- ELASTIC_MOVIES_INDEX - название индекса по фильмам в Elastic
- ELASTIC_GENRES_INDEX - название индекса по жанрам в Elastic
- ELASTIC_PERSONS_INDEX - название индекса по персонам в Elastic
- FAST_API_URL - url тестируемого api


## Запуск в docker
Параметры для запуска в docker прописаны по умолчанию в файле `tests/functional/settings.py`:
