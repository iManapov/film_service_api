import pytest
# from tests.functional.testdata.es_data import es_data


#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`,
#  который следит за запуском и работой цикла событий.


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
@pytest.mark.asyncio
async def test_genres(es_write_genres, make_get_request, query_data, expected_answer):
    await es_write_genres()
    # 1. Запрашиваем данные из ES по API
    response = await make_get_request('/genres', query_data)

    # 2. Проверяем ответ
    assert response.status == expected_answer['status']
    response_body = await response.json()
    if response.status == 200:
        assert len(response_body) == expected_answer['length']
    elif response.status == 422:
        assert response_body['detail'][0]['type'] == expected_answer['error_msg']


@pytest.mark.asyncio
async def test_genres_id(es_delete_by_id, make_get_request):
    # 1. Запрашиваем данные из API
    response = await make_get_request('/genres', {'page[size]': 1})
    assert response.status == 200
    body = await response.json()
    genre_id = body[0]['uuid']

    # 2. Запрашиваем данные из API по определенному id
    response = await make_get_request(f'/genres/{genre_id}')
    assert response.status == 200
    body = await response.json()
    assert body['uuid'] == genre_id

    # 3. Удаляем из Elastic запись с genre_id
    es_delete_by_id('genres', genre_id)

    # 4. Заново запрашиваем данные из API по определенному id
    response = await make_get_request(f'/genres/{genre_id}')
    assert response.status == 200
    body = await response.json()
    assert body['uuid'] == genre_id



