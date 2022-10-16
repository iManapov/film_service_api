import pytest
from tests.functional.testdata.person_data import correct_id


pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'Eduardo Durant'},
                {'status': 200}
        ),
    ]
)
async def test_person_for_films(make_get_request, es_write_data, query_data, expected_answer):
    # 1. Генерируем данные для ES
    person_id = correct_id

    # 3. Запрашиваем данные из ES по API
    body, status = await make_get_request(f'/api/v1/persons/{person_id}/film')

    # 4. Проверяем ответ
    assert status == expected_answer['status']
    # assert len(await response.json()) == expected_answer['length']


