import random
import uuid
import json

import pytest

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings
from tests.functional.testdata.film_data import es_film_data
from tests.functional.testdata.genre_data import es_genre_data
from tests.functional.testdata.es_mapping import es_movies_index, es_genres_index, es_persons_index
from tests.functional.testdata.person_data import es_data_persons

@pytest.fixture(scope="session")
async def es_client():
    """
    Фикстура для установления соединения с ES
    на время тестов
    """
    client = AsyncElasticsearch(
        hosts=f"{test_settings.elastic_host}:{test_settings.elastic_port}",
        validate_cert=False,
        use_ssl=False,
    )
    yield client
    await client.close()


async def es_clear_data_from_index(es_client: AsyncElasticsearch, es_index_name: str):
    if await es_client.indices.exists(index=es_index_name):
        await es_client.delete_by_query(
            index=es_index_name, body={"query": {"match_all": {}}}
        )


@pytest.fixture(autouse=True, scope="session")
async def es_clear_data(es_client: AsyncElasticsearch):
    """
    Фикстура для удаления данных из ES
    Срабатывает один раз в начале тестов
    """
    await es_clear_data_from_index(es_client, test_settings.elastic_movies_index)
    await es_clear_data_from_index(es_client, test_settings.elastic_genres_index)
    await es_clear_data_from_index(es_client, test_settings.elastic_persons_index)


async def es_write_data_to_index(
    es_client: AsyncElasticsearch,
    es_index_name: str,
    es_index_schema: dict,
    data: list[dict],
):
    """
    Функция для записи тестовых данных в индекс

    :param es_client: фикстура клиента elasticsearch
    :param es_index_name: название индекса в elasticsearch
    :param es_index_schema: схема индекса в elasticsearch
    :param data: тестовые данные
    """

    bulk_query = []
    list_with_films_id = []
    for row in data:
        bulk_query.extend(
            [
                json.dumps(
                    {
                        "index": {
                            "_index": es_index_name,
                            "_id": row[test_settings.elastic_id_field],
                        }
                    }
                ),
                json.dumps(row),
            ]
        )
        if es_index_name == es_movies_index:
            list_with_films_id.append(row['id'])
    str_query = "\n".join(bulk_query) + "\n"
    print(f"Writing index {es_index_name}")
    if not await es_client.indices.exists(index=es_index_name):
        await es_client.indices.create(index=es_index_name, body=es_index_schema)
    print(f"Writing index {es_index_name}")
    response = await es_client.bulk(str_query, refresh=True)
    if response["errors"]:
        raise Exception("Ошибка записи данных в Elasticsearch")
    return list_with_films_id


@pytest.fixture(autouse=True, scope="session")
async def es_write_data(es_client: AsyncElasticsearch):
    """
    Фикстура для заполнения ES данными
    Срабатывает один раз в начале тестов
    """

    list_with_films_id = await es_write_data_to_index(
        es_client, test_settings.elastic_movies_index, es_movies_index, es_film_data
    )
    await es_write_data_to_index(
        es_client, test_settings.elastic_genres_index, es_genres_index, es_genre_data
    )
    await es_write_data_for_person(es_client, list_with_films_id, es_data_persons)


async def es_write_data_for_person(es_client: AsyncElasticsearch, list_with_films_id: list, person_data: list[dict]):
    bulk_query = []
    for row in person_data:
        if list_with_films_id:
            row['film_ids'] = [random.choice(list_with_films_id) for _ in range(random.randint(1, 4))]
        else:
            row['film_ids'] = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
        bulk_query.extend([
            json.dumps({'index': {'_index': test_settings.elastic_persons_index, '_id': row[test_settings.elastic_id_field]}}),
            json.dumps(row)
        ])
    str_query = '\n'.join(bulk_query) + '\n'

    if not await es_client.indices.exists(index=test_settings.elastic_persons_index):
        await es_client.indices.create(
            index=test_settings.elastic_persons_index,
            body=es_persons_index
        )

    response = await es_client.bulk(str_query, refresh=True)

    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch')
    return person_data[random.randint(0, len(person_data)-1)]['id']
