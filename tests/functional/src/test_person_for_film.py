import pytest
from tests.functional.testdata.person_data import es_data_persons, correct_id
from tests.functional.testdata.film_data import es_film_data
from tests.functional.settings import test_settings


@pytest.mark.parametrize(
    'expected_answer',
    [
        (

                {'status': 200}
        ),
    ]
)
@pytest.mark.asyncio
async def test_person_for_films(make_get_request, es_write_data, expected_answer):
    # 1. Генерируем данные для ES
    person_id = correct_id

    # 2. Запрашиваем данные из ES по API
    body, status = await make_get_request(f'/api/v1/persons/{person_id}/film')

    # 3. Проверяем ответ
    assert status == expected_answer['status']


