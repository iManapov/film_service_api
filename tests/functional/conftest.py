import asyncio
import json

import pytest

from tests.functional.settings import test_settings


pytest_plugins = (
    "tests.functional.fixtures.elastic",
    "tests.functional.fixtures.http",
    "tests.functional.fixtures.redis",
)


@pytest.fixture(scope="session")
def event_loop():
    """
    Переопределенная стандартная фикстура
    для создания цикла событий
    на время выполнения тестов
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
