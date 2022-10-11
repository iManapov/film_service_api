import json

import asyncio, aiohttp
import aioredis

import pytest

from tests.functional.settings import test_settings
from tests.functional.testdata.film_data import es_film_data
from tests.functional.testdata.genre_data import es_genre_data

from elasticsearch import AsyncElasticsearch
from aioredis import Redis


@pytest.fixture(scope="session")
def event_loop():
    """
    Переопределенная стандартная фикстура
    для создания цикла событий
    на время выполнения тестов
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session')
async def es_client():
    """
    Фикстура для установления соединения с ES
    на время тестов
    """
    client = AsyncElasticsearch(
        hosts=f'{test_settings.elastic_host}:{test_settings.elastic_port}',
        validate_cert=False,
        use_ssl=False
    )
    yield client
    await client.close()

@pytest.fixture(autouse=True,
                scope='session')
async def es_clear_data(es_client: AsyncElasticsearch):
    """
    Фикстура для удаления данных из ES
    Срабатывает один раз в начале тестов
    """
    await es_client.delete_by_query(
        index=test_settings.elastic_movies_index,
        body={"query": {"match_all": {}}}
    )

@pytest.fixture(autouse=True,
                scope='session')
async def es_write_data(es_client: AsyncElasticsearch):
    """
    Фикстура для заполнения ES данными
    Срабатывает один раз в начале тестов
    """
    print('done')
    bulk_query = []

    for row in es_film_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': test_settings.elastic_movies_index,
                                  '_id': row[test_settings.elastic_id_field]}
                        }),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'
    response = await es_client.bulk(str_query, refresh=True)

    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch')

@pytest.fixture(scope='session')
async def http_session():
    """
    Фикстура для установления соединения по
    HTTP на время тестов
    """
    session = aiohttp.ClientSession()
    yield session
    await session.close()

@pytest.fixture
def make_get_request(http_session: aiohttp.ClientSession):
    """
    Фикстура для выполнения запроса к API
    """
    async def inner(url, query_data = None):
        async with http_session.get(url, params=query_data) as response:
            body = await response.json()
            status = response.status
            return body, status
    return inner

@pytest.fixture(scope='session')
async def redis_client():
    """
    Фикстура для установления соединения с Redis
    на время тестов
    """
    client = await aioredis.create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port),
        minsize=10,
        maxsize=20
    )
    yield client
    client.close()
    await client.wait_closed()

@pytest.fixture
def check_cache(redis_client: Redis):
    """
    Фикстура для проверки результата запроса в кеше
    """
    async def inner(url: str):
        cache_data = await redis_client.get(url)
        if cache_data:
            return json.loads(cache_data)
        return None
    return inner
