# Код функциональных тестоа

## Локальный запуск
Для запуска тестов локально необходимо создать файл `tests/functional/.env` со следующими параметрами:

- PROJECT_NAME - название проекта
- REDIS_HOST - хост redis
- REDIS_PORT - порт redis
- ELASTIC_HOST - хост Elasticsearch
- ELASTIC_PORT - порт Elasticsearch
- ES_INDEX - название индекса в Elastic
- ES_ID_FIELD - название поля с id в Elastic
- SERVICE_URL - url тестируемого api


## Запуск в docker
Параметры для запуска в docker прописаны по умолчанию в файле `tests/functional/settings.py`:
