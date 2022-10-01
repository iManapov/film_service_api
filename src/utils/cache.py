import json

from dataclasses import dataclass
from typing import Union

from fastapi import Request
from aioredis import Redis


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


@dataclass
class Cache:
    """
    Класс для кеширования в Redis
    В качестве ключа используется текущий запрошенный URL
    URL получаем из request
    """
    request: Request
    redis: Redis

    async def set(self, data: dict):
        """
        Сохранение в кеш

        @param data: данные для сохранения в кеш
        """
        current_url = f"{self.request['path']}?{self.request['query_string']}"
        await self.redis.set(current_url,
                             json.dumps(data),
                             expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def get(self) -> Union[dict, None]:
        """
        Извлечение из кеша

        @return: данные из кеша
        """
        current_url = f"{self.request['path']}?{self.request['query_string']}"
        data = await self.redis.get(current_url)
        if not data:
            return None
        return json.loads(data)
