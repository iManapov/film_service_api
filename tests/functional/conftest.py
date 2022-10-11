import json
import pytest
from elasticsearch import AsyncElasticsearch
import asyncio
from tests.functional.settings import test_settings
from tests.functional.testdata.es_mapping import es_movies_index, es_genres_index
from tests.functional.testdata.es_data import movies_data, genres_data
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
    # await es_write_data(client, test_settings.es_movies_index, es_movies_index, movies_data)
    # await es_write_data(client, test_settings.es_genres_index, es_genres_index, genres_data)
    # client = AsyncElasticsearch(hosts='localhost:9200', validate_cert=False, use_ssl=False)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def api_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture()
def make_get_request(api_session):
    async def inner(endpoint: str, query_data: dict = {}):
        url = test_settings.service_url + '/api/v1' + endpoint
        response = await api_session.get(url, params=query_data)
        return response
    return inner



@pytest.fixture
def es_write_genres(es_client):
    async def inner():
        bulk_query = []
        for row in genres_data:
            bulk_query.extend([
                json.dumps({'index': {'_index': test_settings.es_genres_index, '_id': row[test_settings.es_id_field]}}),
                json.dumps(row)
            ])
        str_query = '\n'.join(bulk_query) + '\n'

        if not await es_client.indices.exists(index=test_settings.es_genres_index):
            await es_client.indices.create(
                index=test_settings.es_genres_index,
                body=es_genres_index
            )

        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def es_write_movies(es_client):
    async def inner():
        bulk_query = []
        for row in movies_data:
            bulk_query.extend([
                json.dumps({'index': {'_index': test_settings.es_movies_index, '_id': row[test_settings.es_id_field]}}),
                json.dumps(row)
            ])
        str_query = '\n'.join(bulk_query) + '\n'

        if not await es_client.indices.exists(index=test_settings.es_movies_index):
            await es_client.indices.create(
                index=test_settings.es_movies_index,
                body=es_movies_index
            )

        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def es_delete_by_id(es_client):
    async def inner(es_index_name, entity_id):
        await es_client.delete(index=es_index_name, id=entity_id, doc_type='_doc')
    return inner
