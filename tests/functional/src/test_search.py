import pytest

from urllib.parse import urlencode

from tests.functional.testdata.search_data import search_test_data


pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'url, query_data, expected_answer',
    search_test_data
)
async def test_search(make_get_request,
                      check_cache,
                      url: str,
                      query_data: dict,
                      expected_answer: dict):

    body, status = await make_get_request(url, query_data)

    assert status == expected_answer['status']
    if status == 200:
        cache_response = await check_cache(
            f"{url}?b'{urlencode(query_data)}'"
        )
        assert len(body) == expected_answer['length']
        assert len(cache_response) == expected_answer['length']