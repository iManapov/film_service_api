import pytest


pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'page[size]': 22},
            {'status': 200, 'length': 22}
        ),
        (
            {'page[size]': -1},
            {'status': 422, 'error_msg': 'value_error.number.not_ge'}
        ),
        (
            {'page[size]': 400},
            {'status': 422, 'error_msg': 'value_error.number.not_le'}
        ),
        (
            {'page[number]': -3},
            {'status': 422, 'error_msg': 'value_error.number.not_ge'}
        ),
        (
            {'page[number]': 100},
            {'status': 200, 'length': 0}
        ),
        (
            {'page[number]': 2, 'page[size]': 8, 'sort': 'name'},
            {'status': 200, 'length': 8}
        ),
        (
            {'page[number]': 2, 'page[size]': 8, 'sort': 'dfdskfjdshfjds'},
            {'status': 400}
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

    if status == 200:
        assert len(body) == expected_answer['length']
    elif status == 422:
        assert body['detail'][0]['type'] == expected_answer['error_msg']


async def test_genres_id(check_cache, make_get_request):
    """
    Тест для проверки выдачи конкретного жанра по id

    :param es_delete_by_id: фикстура для удаления записи в elasticsearch
    :param make_get_request: фикстура для get запросов
    """

    # 1. Запрашиваем данные из API
    body, status = await make_get_request('/api/v1/genres', {'page[size]': 1})
    assert status == 200
    genre_id = body[0]['uuid']

    # 2. Запрашиваем данные из API по определенному id
    body, status = await make_get_request(f'/api/v1/genres/{genre_id}')
    assert status == 200

    # 3. Если статус = 200, проверяем запись с genre_id
    if status == 200:
        cache_response = await check_cache(f"/api/v1/genres/{genre_id}?b''")
        assert cache_response['_source']['id'] == genre_id
