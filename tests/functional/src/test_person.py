import pytest

from tests.functional.settings import test_settings
from tests.functional.testdata.person_data import es_data_persons, correct_id


#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`,
#  который следит за запуском и работой цикла событий.


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    [
        (
                '/api/v1/persons/search',
                {'query': 'Eduardo Durant'},
                {'status': 200, 'length': 30}
        ),
        (
                '/api/v1/persons/search',
                {'query': 'Mashed potato'},
                {'status': 200, 'length': 0}
        ),
        (
                '/api/v1/persons/search',
                {'query': 'Eduardo Durant', 'page[size]': 60, "page[number]": -1},
                {'status': 422}
        ),
        (
                '/api/v1/persons',
                {'page[size]': 60, "page[number]": -1},
                {'status': 422}
        ),
        (
                '/api/v1/persons',
                {},
                {'status': 200}
        ),
        (
            f'/api/v1/persons/{correct_id}',
            {},
            {'status': 200}
        )
    ]
)
@pytest.mark.asyncio
async def test_person(make_get_request, es_write_data, query_data, expected_answer, url, es_delete_by_id):

    # 3. Запрашиваем данные из ES по API
    body, status = await make_get_request(test_settings.service_url + url, query_data)

    # 4. Проверяем ответ
    assert status == expected_answer['status']
    if hasattr(expected_answer, 'length'):
        assert len(body) == expected_answer['length']


@pytest.mark.asyncio
async def test_redis_person_id(es_delete_by_id, make_get_request):
    body, status = await make_get_request(test_settings.service_url + '/api/v1/persons', {'page[size]': 1})
    assert status == 200
    person_id = body[0]['uuid']
    # 2. Запрашиваем данные из API по определенному id
    body, status = await make_get_request(test_settings.service_url + f'/api/v1/persons/{person_id}')
    assert status == 200
    assert body['uuid'] == person_id

    # 3. Удаляем из Elastic запись с person_id
    es_delete_by_id('persons', person_id)

    # 4. Заново запрашиваем данные из API по определенному id
    body, status = await make_get_request(test_settings.service_url + f'/api/v1/persons/{person_id}')
    assert status == 200
    assert body['uuid'] == person_id


