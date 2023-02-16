import uuid

from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from src.services.person import PersonService, get_person_service
from src.models.person import BasePersonApi
from src.models.film import BaseFilmApi
from src.core.params import params
from src.core.error_messages import error_msgs


router = APIRouter()


@router.get('/search',
            response_model=list[BasePersonApi],
            summary="Person search",
            description="Providing a fuzzy search on persons",
            )
async def search_persons(
        sort: Optional[str] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        query: Optional[str] = params.query,
        person_service: PersonService = Depends(get_person_service)
) -> Optional[list[BasePersonApi]]:
    """
    Returns search result by person name

    :param sort: sorting field
    :param limit: the number of films on one page
    :param page: page number
    :param query: search query
    :param person_service: persons service
    :return: information about person
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
            summary="Film list with this person",
            description="Providing film search with person_id",
            )
async def persons_film(
        person_id: uuid.UUID = params.person_id,
        person_service: PersonService = Depends(get_person_service)
) -> Optional[list[BaseFilmApi]]:
    """
    Returns film list with person_id

    :param person_id: person uuid
    :param person_service: persons service
    :return: films list
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
            summary="Information about person with person_id",
            description="Detailed information about person with person_id",
            )
async def person_details(
        person_id: uuid.UUID = params.person_id,
        person_service: PersonService = Depends(get_person_service)
) -> BasePersonApi:
    """
    Returns information about person

    :param person_id: person uuid
    :param person_service: persons service
    :return: information about person
    """

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
            summary="Get a few persons",
            description="Short information about a few persons",
            )
async def get_persons(
        sort: Optional[str] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        person_service: PersonService = Depends(get_person_service)
) -> Optional[list[BasePersonApi]]:
    """
    Returns information about a few persons

    :param sort: sorting field
    :param limit: the number of films on one page
    :param page: page number
    :param person_service: persons service
    :return: a few persons with short info
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
