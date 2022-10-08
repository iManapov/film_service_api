import json
import pytest
from elasticsearch import AsyncElasticsearch
import asyncio
from tests.functional.settings import test_settings
from tests.functional.testdata.es_mapping import es_index
import aiohttp

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=f'{test_settings.es_host}:{test_settings.es_port}',
                                validate_cert=False,
                                use_ssl=False)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def api_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture()
def make_get_request(api_session):
    async def inner(endpoint: str, query_data: dict):
        url = test_settings.service_url + '/api/v1' + endpoint
        response = await api_session.get(url, params=query_data)
        return response
        # async with api_session.get(url, params=query_data) as response:
        #     return response
    return inner


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: list[dict]):
        bulk_query = []
        for row in data:
            bulk_query.extend([
                json.dumps({'index': {'_index': test_settings.es_index, '_id': row[test_settings.es_id_field]}}),
                json.dumps(row)
            ])
        str_query = '\n'.join(bulk_query) + '\n'

        if not await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.create(
                index=test_settings.es_index,
                body=es_index
            )

        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner
