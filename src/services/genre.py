import uuid
from typing import Optional, Tuple

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import RequestError
from fastapi import Depends, Request

from src.services.views import Views
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.genre import Genre
from src.utils.cache import AbstractCache, RedisCache
from src.utils.sort_string import clear_sort_string
from src.utils.search import AbstractSearchEngine, ElasticSearch


class GenreService(Views):
    def __init__(self, cache: AbstractCache, elastic: AbstractSearchEngine):
        self.elastic = elastic
        self.cache = cache

    async def get_genre_by_id(self, genre_id: uuid.UUID) -> Optional[Genre]:
        """
        Returns genre by uuid

        :param genre_id: genre uuid
        :return: Genre object
        """

        genre = await self.get_record_by_id(genre_id, 'genres')
        return Genre(**genre['_source']) if genre else None

    async def get_genres(
            self,
            sort: Optional[str] = None,
            limit: Optional[int] = 50,
            page: Optional[int] = 1,
    ) -> Tuple[Optional[list[Genre]], list[str]]:
        """
        Returns Genres list

        :param sort: sorting field
        :param limit: the number of films on one page
        :param page: page number
        :return: list of Genre objects
        """

        errors = []
        query_ = None

        genres = await self.cache.get()

        if not genres:
            sort = clear_sort_string(sort, 'name')
            try:
                genres = await self.elastic.search(
                    index='genres',
                    body=query_,
                    size=limit,
                    sort=sort,
                    page=page
                )

                await self.cache.set(genres)

            except RequestError:
                genres = None
                errors.append('Requested parameters has errors')

        return genres, errors


def get_genre_service(
        request: Request,
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    """
    GenreService provider,
    using 'Depends', it says that it needs Redis and Elasticsearch
    """
    return GenreService(RedisCache(redis, request), ElasticSearch(elastic))
