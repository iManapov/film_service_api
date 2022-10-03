import uuid

from http import HTTPStatus
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException

from services.person import PersonService, get_person_service
from models.person import BasePersonApi
from models.film import BaseFilmApi


router = APIRouter()


@router.get('/search',
            response_model=list[BasePersonApi],
            summary="Поиск по персоналиям",
            description="Осуществляет нечеткий поиск по персоналиям",
            )
async def persons(sort: Union[str, None] = None,
                  limit: Optional[int] = 50,
                  page: Optional[int] = 1,
                  query: Optional[str] = None,
                  person_service: PersonService = Depends(get_person_service)) -> \
        Union[list[BasePersonApi], None]:
    """
    Возвращает результаты поиска по имени персоналии.

    @param sort: имя поля по которому идет сортировка
    @param limit: количество записей на странице
    @param page: номер страницы
    @param query: поисковый запрос
    @param person_service:
    @return: Данные по персоналиям
    """

    persons, errors = await person_service.get_persons(sort=sort,
                                                       limit=limit,
                                                       page=page,
                                                       query=query
                                                       )

    if errors:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=errors)

    search_person_list = [
        BasePersonApi(uuid=person['_source']['id'],
                      name=person['_source']['name'],
                      role=person['_source']['role'],
                      film_ids=person['_source']['film_ids']
                      )
        for person in persons
    ]

    return search_person_list


@router.get('/{person_id}/film',
            response_model=list[BaseFilmApi],
            summary="Список фильмов персоналии",
            description="Осуществляет получение список фильмов персоналии person_id",
            )
async def persons_film(person_id: uuid.UUID,
                       person_service: PersonService = Depends(get_person_service)) -> \
        Union[list[BaseFilmApi], None]:
    """
    Возвращает список фильмом с участием персоналии person_id.

    @param person_id: id персоналии
    @param person_service:
    @return: Данные по фильмам
    """

    films, errors = await person_service.get_persons_film(person_id=person_id)

    if errors:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=errors)

    persons_film_list = [
        BaseFilmApi(uuid=film['_source']['id'],
                    title=film['_source']['title'],
                    imdb_rating=film['_source']['imdb_rating']
                    )
        for film in films
    ]
    return persons_film_list


@router.get('/{person_id}',
            response_model=BasePersonApi,
            summary="Информация по одной персоналии",
            description="Детальная информация по отдельной персоналии",
            )
async def person_details(person_id: uuid.UUID,
                         person_service: PersonService =
                         Depends(get_person_service)) -> BasePersonApi:
    """Возвращает информацию по одной персоналии."""

    person = await person_service.get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='person not found')
    return BasePersonApi(uuid=person.id,
                         name=person.name,
                         role=person.role,
                         film_ids=person.film_ids
                         )
