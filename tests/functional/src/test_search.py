import pytest
from tests.functional.testdata.es_data import es_data


#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`,
#  который следит за запуском и работой цикла событий.


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star'},
                {'status': 200, 'length': 50}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(make_get_request, es_write_data, query_data, expected_answer):
    # 1. Генерируем данные для ES
    await es_write_data(es_data)

    # 3. Запрашиваем данные из ES по API
    response = await make_get_request('/films/search', query_data)

    # 4. Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(await response.json()) == expected_answer['length']
