from http import HTTPStatus
import pytest

from tests.functional.testdata.person_data import correct_id


pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'expected_answer',
    [
        (
            {'status': HTTPStatus.OK}
        ),
    ]
)
async def test_person_for_films(make_get_request, expected_answer):
    # 1. Генерируем данные для ES
    person_id = correct_id

    # 2. Запрашиваем данные из ES по API
    body, status = await make_get_request(f'/api/v1/persons/{person_id}/film')

    # 3. Проверяем ответ
    assert status == expected_answer['status']
