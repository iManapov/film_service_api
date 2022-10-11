import uuid
import pytest

from urllib.parse import quote_plus as encode

from tests.functional.settings import test_settings
from tests.functional.testdata.film_data import one_film_test_data, list_film_test_data


@pytest.mark.parametrize(
    'film_uuid, expected_answer',
    one_film_test_data
)
@pytest.mark.asyncio
async def test_one_film(make_get_request,
                        check_cache,
                        film_uuid: uuid.UUID,
                        expected_answer: dict):
    """
    Тест для проверки выдачи информации
    по одному фильму
    """
    body, status = await make_get_request(
        test_settings.service_url + '/api/v1/films/' + str(film_uuid)
    )

    assert status == expected_answer['status']

    if status == 200:
        cache_response = await check_cache(f"/api/v1/films/{str(film_uuid)}?b''")
        assert body == expected_answer['response']
        assert cache_response['_source']['id'] == expected_answer['response']['uuid']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    list_film_test_data
)
@pytest.mark.asyncio
async def test_list_film(make_get_request,
                         check_cache,
                         query_data: dict,
                         expected_answer: dict):
    """
    Тест для проверки выдачи информации
    по нескольким фильмам
    """
    body, status = await make_get_request(
        test_settings.service_url + '/api/v1/films/',
        query_data
    )

    assert status == expected_answer['status']
    if status == 200:
        query_string = '&'.join('{}={}'.format(encode(key), value)
                                for key, value in query_data.items())
        cache_response = await check_cache(
            f"/api/v1/films/?b'{query_string}'"
        )
        assert len(body) == expected_answer['length']
        assert len(cache_response) == expected_answer['length']
