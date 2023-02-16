import json

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union

from fastapi import Request
from aioredis import Redis

from src.core.config import settings


class AbstractCache(ABC):
    """Abstract class for cache"""

    @abstractmethod
    def set(self, data: dict):
        pass

    @abstractmethod
    def get(self):
        pass


@dataclass
class RedisCache(AbstractCache):
    """
    Class for Redis cache
    Requested URL uses as key
    URL is getting from request
    """

    redis: Redis
    request: Request

    async def set(self, data: dict):
        """
        Write record to cache

        :param data: cache data
        """

        current_url = f"{self.request['path']}?{self.request['query_string']}"
        await self.redis.set(
            current_url,
            json.dumps(data),
            ex=settings.FILM_CACHE_EXPIRE_IN_SECONDS
        )

    async def get(self) -> Union[dict, None]:
        """
        Returns cache data by key

        :return: cache data
        """

        current_url = f"{self.request['path']}?{self.request['query_string']}"
        data = await self.redis.get(current_url)
        if not data:
            return None
        return json.loads(data)
