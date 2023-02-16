import uuid

from typing import Optional, Union, Tuple

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.exceptions import RequestError
from fastapi import Depends, Request, Query

from src.services.views import Views
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import Film
from src.utils.cache import AbstractCache, RedisCache
from src.utils.sort_string import clear_sort_string
from src.utils.search import AbstractSearchEngine, ElasticSearch


class FilmService(Views):
    def __init__(self, cache: AbstractCache, elastic: AbstractSearchEngine):
        self.elastic = elastic
        self.cache = cache

    async def get_film_by_id(self, film_id: uuid.UUID) -> Optional[Film]:
        """
        Returns film by id

        :param film_id: film uuid
        :return: Film object or None
        """

        film = await self.get_record_by_id(film_id, 'movies')
        return Film(**film['_source']) if film else None

    async def get_films(
            self,
            sort: Optional[str] = None,
            limit: Optional[int] = 50,
            page: Optional[int] = 1,
            genre: Optional[Union[uuid.UUID, list[uuid.UUID], None]] = Query(default=None),
            query: Optional[str] = None
    ) -> Tuple[Optional[list[Film]], list[str]]:
        """
        Returns list of Films

        :param sort: sorting field
        :param limit: the number of films on one page
        :param page: page number
        :param query: search query
        :param genre: genre uuid to filter for
        :return: Films list
        """

        errors = []
        query_ = None

        films = await self.cache.get()

        if not films:
            sort = clear_sort_string(sort, 'title')

            if genre:
                if isinstance(genre, uuid.UUID):
                    genre = [str(genre)]

                genre_query = [
                    {"term": {"genre.id": str(one_genre)}}
                    for one_genre in genre
                ]

                query_ = {
                    "query": {
                        "nested": {
                            "path": "genre",
                            "query": {
                                "bool": {
                                    "should": genre_query
                                }
                            }
                        }
                    }
                }

            if query:
                query_ = {
                    "query": {
                        "match": {
                            "title": {
                                "query": query,
                                "fuzziness": "auto"
                            }
                        }
                    }
                }

            try:
                films = await self.elastic.search(
                    index='movies',
                    body=query_,
                    size=limit,
                    sort=sort,
                    page=page
                )

                await self.cache.set(films)

            except RequestError:
                films = None
                errors.append('Requested parameters has errors')

        return films, errors

    async def get_same_films(
            self,
            film_id: uuid.UUID,
            sort: Optional[str] = None,
            limit: Optional[int] = 50,
            page: Optional[int] = 1,
    ) -> Tuple[Optional[list[Film]], list[str]]:
        """
        Returns similar films

        :param film_id: film uuid
        :param sort: sorting field
        :param limit: the number of films on one page
        :param page: page number
        """

        try:
            film = await self.elastic.get('movies', film_id)

            genre = [
                genre['id']
                for genre in film['_source']['genre']
            ]

        except NotFoundError:
            return

        result = await self.get_films(
            sort=sort,
            limit=limit,
            page=page,
            genre=genre
        )

        return result


def get_film_service(
        request: Request,
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    """
    FilmService provider,
    using 'Depends', it says that it needs Redis and Elasticsearch
    """
    return FilmService(RedisCache(redis, request), ElasticSearch(elastic))
