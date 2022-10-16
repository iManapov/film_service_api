import uuid

from typing import Optional, Union, Tuple

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.exceptions import RequestError
from fastapi import Depends, Request

from src.services.views import Views
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.person import Person
from src.models.film import BaseFilmApi
from src.utils.cache import AbstractCache, RedisCache
from src.utils.sort_string import clear_sort_string
from src.utils.search import AbstractSearchEngine, ElasticSearch


class PersonService(Views):
    def __init__(self, cache: AbstractCache, elastic: AbstractSearchEngine):
        self.elastic = elastic
        self.cache = cache

    async def get_person_by_id(self, person_id: uuid.UUID) -> Optional[Person]:
        """
        Получаем персону по uuid

        @param person_id: uuid персоны
        @return: объект-персона
        """
        person = await self.get_record_by_id(person_id, 'persons')
        person = Person(**person['_source'])
        return person

    async def get_persons(
            self,
            sort: Optional[str] = None,
            limit: Optional[int] = 50,
            page: Optional[int] = 1,
            query: Optional[str] = None
    ) -> Tuple[Union[list[Person], None], list[str]]:
        """
        Получает список персоналий по запросу query

        @param sort: имя поля по которому идет сортировка
        @param limit: количество записей на странице
        @param page: номер страницы
        @param query: поисковый запрос
        @return: Данные по персоналиям
        """

        errors = []
        query_ = None

        persons = await self.cache.get()

        if not persons:
            sort = clear_sort_string(sort, 'name')

            if query:
                query_ = {
                    "query": {
                        "query_string": {
                            "default_field": "name",
                            "query": query
                        }
                    }
                }

            try:
                persons = await self.elastic.search(
                    index='persons',
                    body=query_,
                    size=limit,
                    sort=sort,
                    page=page
                )
                await self.cache.set(persons)

            except RequestError:
                persons = None
                errors.append('В запрашиваемых параметрах содержатся ошибки')

        return persons, errors

    async def get_persons_film(self, person_id: uuid.UUID) \
            -> Tuple[Union[list[BaseFilmApi], None], list[str]]:
        """
        Метод получения фильмов с участием персоналии с person_id.

        @param person_id: id персоналии
        @return: список фильмов персоналии
        """

        errors = []

        films = await self.cache.get()

        if not films:
            films = []
            person = await self.get_person_by_id(person_id)
            if not person:
                errors.append('Wrong user uuid')
                return None, errors
            for film_id in person.film_ids:
                try:
                    film = await self.elastic.get('movies', film_id)
                    films.append(film)
                except NotFoundError:
                    pass
        await self.cache.set(films)

        return films, errors


def get_person_service(
        request: Request,
        redis: RedisCache = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    """
    Провайдер PersonService,
    с помощью Depends он сообщает, что ему необходимы Redis и Elasticsearch
    """
    return PersonService(RedisCache(redis, request), ElasticSearch(elastic))
