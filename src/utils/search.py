
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union, List

from elasticsearch import AsyncElasticsearch


class AbstractSearchEngine(ABC):
    """
    Абстрактный класс для реализации полнотекстового поиска
    """

    @abstractmethod
    def search(self, index, body, size, sort, page):
        pass

    @abstractmethod
    def get(self, index, id_record):
        pass


@dataclass
class ElasticSearch(AbstractSearchEngine):
    """
    Класс для обращений к базе данных ElasticSearch.
    """
    elastic: AsyncElasticsearch

    async def get(self, index, id_record) -> Union[dict, None]:
        """
        Получение конкретной записи по индексу и id записи.
        Args:
            index: Запрашиваемый индекс
            id_record: id запрашиваемой записи
        Returns:
            response: Ответ одной записи от БД
        """
        response = await self.elastic.get(index, id_record)
        return response

    async def search(self, index, body, size, sort, page) -> Union[List[dict], None]:
        """
        Args:
            index: Запрашиваемый индекс
            sort: имя поля по которому идет сортировка
            size: количество записей на странице
            page: номер страницы
            body: поисковый запрос
        Returns:
            Список запрашиваемых данных от БД
        """
        response = await self.elastic.search(
            index=index,
            body=body,
            size=size,
            sort=sort,
            from_=size * (page - 1)
        )
        response_body = response['hits']['hits']
        return response_body
