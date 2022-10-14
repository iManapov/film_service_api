import pytest

from urllib.parse import urlencode

from tests.functional.testdata.search_data import search_test_data


@pytest.mark.parametrize(
    'query_data, expected_answer',
    search_test_data
)
@pytest.mark.asyncio
async def test_search(make_get_request,
                      check_cache,
                      query_data: dict,
                      expected_answer: dict):

    body, status = await make_get_request('/api/v1/films/search', query_data)

    assert status == expected_answer['status']
    if status == 200:
        cache_response = await check_cache(
            f"/api/v1/films/search?b'{urlencode(query_data)}'"
        )
        assert len(body) == expected_answer['length']
        assert len(cache_response) == expected_answer['length']
