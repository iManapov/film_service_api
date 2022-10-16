import json

import aioredis
import pytest

from aioredis import Redis

from tests.functional.settings import test_settings


@pytest.fixture(scope="session")
async def redis_client():
    """
    Фикстура для установления соединения с Redis
    на время тестов
    """
    client = await aioredis.create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port), minsize=10, maxsize=20
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
