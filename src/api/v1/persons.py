import uuid

from http import HTTPStatus
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException

from src.services.person import PersonService, get_person_service
from src.models.person import BasePersonApi
from src.models.film import BaseFilmApi
from src.core.params import params
from src.core.error_messages import error_msgs


router = APIRouter()


@router.get('/search',
            response_model=list[BasePersonApi],
            summary="Поиск по персоналиям",
            description="Осуществляет нечеткий поиск по персоналиям",
            )
async def persons(
        sort: Union[str, None] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        query: Optional[str] = params.query,
        person_service: PersonService = Depends(get_person_service)
) -> Union[list[BasePersonApi], None]:
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
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=error_msgs.bad_request)

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
            description="Осуществляет получение списка фильмов персоналии по person_id",
            )
async def persons_film(
        person_id: uuid.UUID = params.person_id,
        person_service: PersonService = Depends(get_person_service)
) -> Union[list[BaseFilmApi], None]:
    """
    Возвращает список фильмом с участием персоналии person_id.

    @param person_id: id персоналии
    @param person_service:
    @return: Данные по фильмам
    """

    films, errors = await person_service.get_persons_film(person_id=person_id)

    if errors:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=error_msgs.bad_request)

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
async def person_details(
        person_id: uuid.UUID = params.person_id,
        person_service: PersonService =
        Depends(get_person_service)
) -> BasePersonApi:
    """Возвращает информацию по одной персоналии."""

    person = await person_service.get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.person_not_found)  # Некорректная ссылка к person_not_found
    return BasePersonApi(uuid=person.id,
                         name=person.name,
                         role=person.role,
                         film_ids=person.film_ids
                         )


@router.get('/',
            response_model=list[BasePersonApi],
            summary="Информация по нескольким персонам",
            description="Краткая информация по нескольким персонам",
            )
async def genres(
        sort: Union[str, None] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        person_service: PersonService = Depends(get_person_service)
) -> Union[list[BasePersonApi], None]:
    """
    Возвращает информацию по нескольким персонам

    @param sort: имя поля по которому идет сортировка
    @param limit: количество записей на странице
    @param page: номер страницы
    @param person_service:
    @return: Данные по жанрам
    """

    persons, errors = await person_service.get_persons(sort=sort, limit=limit, page=page)

    if errors:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=error_msgs.bad_request)

    non_detail_person_list = [
        BasePersonApi(uuid=person['_source']['id'],
                      name=person['_source']['name']
                      )
        for person in persons
    ]

    return non_detail_person_list
