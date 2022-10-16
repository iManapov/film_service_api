from http import HTTPStatus
import pytest


pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'page[size]': 22},
            {'status': HTTPStatus.OK, 'length': 22}
        ),
        (
            {'page[size]': -1},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'error_msg': 'value_error.number.not_ge'}
        ),
        (
            {'page[size]': 400},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'error_msg': 'value_error.number.not_le'}
        ),
        (
            {'page[number]': -3},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'error_msg': 'value_error.number.not_ge'}
        ),
        (
            {'page[number]': 100},
            {'status': HTTPStatus.OK, 'length': 0}
        ),
        (
            {'page[number]': 2, 'page[size]': 8, 'sort': 'name'},
            {'status': HTTPStatus.OK, 'length': 8}
        ),
        (
            {'page[number]': 2, 'page[size]': 8, 'sort': 'dfdskfjdshfjds'},
            {'status': HTTPStatus.BAD_REQUEST}
        )
    ]
)
async def test_genres(make_get_request, query_data, expected_answer):
    """
    Тест для проверки выдачи жанров

    :param make_get_request: фикстура для get запросов
    :param query_data: параметры запроса
    :param expected_answer: ожидаемый результат
    """

    # 1. Запрашиваем данные из ES по API
    body, status = await make_get_request('/api/v1/genres', query_data)

    # 2. Проверяем ответ
    assert status == expected_answer['status']

    if status == HTTPStatus.OK:
        assert len(body) == expected_answer['length']
    elif status == HTTPStatus.UNPROCESSABLE_ENTITY:
        assert body['detail'][0]['type'] == expected_answer['error_msg']


async def test_genres_id(check_cache, make_get_request):
    """
    Тест для проверки выдачи конкретного жанра по id

    :param es_delete_by_id: фикстура для удаления записи в elasticsearch
    :param make_get_request: фикстура для get запросов
    """

    # 1. Запрашиваем данные из API
    body, status = await make_get_request('/api/v1/genres', {'page[size]': 1})
    assert status == HTTPStatus.OK
    genre_id = body[0]['uuid']

    # 2. Запрашиваем данные из API по определенному id
    body, status = await make_get_request(f'/api/v1/genres/{genre_id}')
    assert status == HTTPStatus.OK

    # 3. Если статус = 200, проверяем запись с genre_id
    if status == HTTPStatus.OK:
        cache_response = await check_cache(f"/api/v1/genres/{genre_id}?b''")
        assert cache_response['_source']['id'] == genre_id
