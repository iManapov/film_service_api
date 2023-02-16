import uuid
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

from elasticsearch import NotFoundError

from src.utils.cache import AbstractCache
from src.utils.search import AbstractSearchEngine


class AbstractViewEngine(ABC):
    """Abstract class for services"""

    @abstractmethod
    def get_record_by_id(self, record_id, index):
        pass


@dataclass
class Views(AbstractViewEngine):
    cache: AbstractCache
    elastic: AbstractSearchEngine

    async def get_record_by_id(self, record_id: uuid.UUID, index: str) -> Optional[dict]:
        """
        Returns record by id

        :param record_id: record uuid
        :param index: required index
        :return: record in dict
        """

        record = await self.cache.get()

        if not record:
            try:
                record = await self.elastic.get(index, record_id)
            except NotFoundError:
                return None
            await self.cache.set(record)
        return record
