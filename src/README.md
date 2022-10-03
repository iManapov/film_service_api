# Код FastAPI-приложения

## Локальный запуск
Для запуска api локально необходимо создать файл `core/.env` со следующими параметрами:

- PROJECT_NAME - название проекта
- REDIS_HOST - хост redis
- REDIS_PORT - порт redis
- ELASTIC_HOST - хост Elasticsearch
- ELASTIC_PORT - порт Elasticsearch


## Запуск в docker
Для запуска api через docker compose необходимо создать файл `core/docker.env` со следующими параметрами:

- PROJECT_NAME - название проекта
- REDIS_HOST - хост redis
- REDIS_PORT - порт redis
- ELASTIC_HOST - хост Elasticsearch
- ELASTIC_PORT - порт Elasticsearch