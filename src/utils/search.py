from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, List

from elasticsearch import AsyncElasticsearch


class AbstractSearchEngine(ABC):
    """Abstract class to implement full text search"""

    @abstractmethod
    def search(self, index, body, size, sort, page):
        pass

    @abstractmethod
    def get(self, index, id_record):
        pass


@dataclass
class ElasticSearch(AbstractSearchEngine):
    """Class to interact with ElasticSearch"""

    elastic: AsyncElasticsearch

    async def get(self, index, id_record) -> Optional[dict]:
        """
        Returns record by record id in index

        :param index: index in ElasticSearch
        :param id_record: record id
        """

        response = await self.elastic.get(index, id_record)
        return response

    async def search(self, index, body, size, sort, page) -> Optional[List[dict]]:
        """
        Returns search result

        :param index: index in ElasticSearch
        :param body: search body
        :param size: page size
        :param sort: sorting field
        :param page: page number
        :return: search result
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
