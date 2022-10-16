import pytest
import aiohttp

from tests.functional.settings import test_settings


@pytest.fixture(scope="session")
async def http_session():
    """
    Фикстура для установления соединения по
    HTTP на время тестов
    """
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(http_session: aiohttp.ClientSession):
    """
    Фикстура для выполнения запроса к API
    """
    async def inner(url: str, query_data: dict = None):
        url = test_settings.service_url + url
        async with http_session.get(url, params=query_data) as response:
            body = await response.json()
            status = response.status
            return body, status

    return inner