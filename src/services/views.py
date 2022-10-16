import uuid
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

from elasticsearch import NotFoundError

from src.utils.cache import AbstractCache
from src.utils.search import AbstractSearchEngine


class AbstractViewEngine(ABC):
    """
    Абстрактный класс для реализации отдачи данных сервисом
    """

    @abstractmethod
    def get_record_by_id(self, record_id, index):
        pass


@dataclass
class Views(AbstractViewEngine):
    cache: AbstractCache
    elastic: AbstractSearchEngine

    async def get_record_by_id(self, record_id: uuid.UUID, index: str) -> Optional[dict]:
        """
        Получаем запись по uuid

        @param record_id: uuid записи
        @param index: Запрашиваемый индекс
        @return: запись в виде словаря
        """
        record = await self.cache.get()

        if not record:
            try:
                record = await self.elastic.get(index, record_id)
            except NotFoundError:
                return None
            await self.cache.set(record)
        return record
