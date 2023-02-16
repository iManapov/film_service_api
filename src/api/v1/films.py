import uuid

from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError, MissingTokenError

from src.services.film import FilmService, get_film_service
from src.models.film import BaseFilmApi, DetailFilmApi
from src.core.params import params
from src.core.error_messages import error_msgs


router = APIRouter()


@router.get('/search',
            response_model=list[BaseFilmApi],
            summary="Film search",
            description="Providing a fuzzy search on films",
            )
async def search_films(
        sort: Optional[str] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        query: Optional[str] = params.query,
        film_service: FilmService = Depends(get_film_service)
) -> Optional[list[BaseFilmApi]]:
    """
    Returns search result by film name

    :param sort: sorting field
    :param limit: the number of films on one page
    :param page: page number
    :param query: search query
    :param film_service: film service
    :return: film data
    """

    films, errors = await film_service.get_films(sort=sort,
                                                 limit=limit,
                                                 page=page,
                                                 query=query,
                                                 genre=None)

    if errors:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=error_msgs.bad_request)

    search_film_list = [
        BaseFilmApi(uuid=film['_source']['id'],
                    title=film['_source']['title'],
                    imdb_rating=film['_source']['imdb_rating']
                    )
        for film in films
    ]

    return search_film_list


@router.get('/same/{film_id}',
            response_model=list[BaseFilmApi],
            summary="Similar films",
            description="Similar films for current film",
            )
async def same_films(
        film_id: uuid.UUID = params.film_id,
        sort: Optional[str] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        film_service: FilmService = Depends(get_film_service)
) -> Optional[list[BaseFilmApi]]:
    """
    Returns similar films for film with film_id

    :param film_id: film uuid
    :param limit: the number of films on one page
    :param page: page number
    :param sort: sorting field
    :param film_service: film service
    :return: Similar film's data
    """

    result = await film_service.get_same_films(
        film_id=film_id,
        sort=sort,
        limit=limit,
        page=page
    )

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.film_not_exist)

    films, errors = result

    if errors:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=error_msgs.bad_request)

    same_film_list = [
        BaseFilmApi(uuid=film['_source']['id'],
                    title=film['_source']['title'],
                    imdb_rating=film['_source']['imdb_rating']
                    )
        for film in films
        if film['_source']['id'] != film_id
    ]

    return same_film_list


@router.get('/',
            response_model=list[BaseFilmApi],
            summary="Get a few films",
            description="A few films with short information",
            )
async def get_all_films(
        sort: Optional[str] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        genre: Optional[list[uuid.UUID]] = params.genre,
        film_service: FilmService = Depends(get_film_service)
) -> Optional[list[BaseFilmApi]]:
    """
    Returns a few films with short information

    :param limit: the number of films on one page
    :param page: page number
    :param sort: sorting field
    :param genre: genre uuid to filter for
    :param film_service: film service
    :return: List of films with short information
    """

    films, errors = await film_service.get_films(sort=sort,
                                                 limit=limit,
                                                 page=page,
                                                 genre=genre)

    if errors:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=error_msgs.bad_request)

    non_detail_film_list = [
        BaseFilmApi(uuid=film['_source']['id'],
                    title=film['_source']['title'],
                    imdb_rating=film['_source']['imdb_rating'],
                    price=film['_source']['price'],
                    tag=film['_source']['tag'],
                    )
        for film in films
    ]

    return non_detail_film_list


@router.get('/{film_id}',
            response_model=DetailFilmApi,
            summary="Information about film",
            description="""
                Detailed information about film
                If a film has the 'subscription_only' tag then access given to only users with the role 'subscriber'
            """
            )
async def film_details(
        film_id: uuid.UUID = params.film_id,
        film_service: FilmService = Depends(get_film_service),
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(bearerFormat='Bearer')),
        authorize: AuthJWT = Depends()
) -> DetailFilmApi:
    """
    Returns detailed information about film with film_id

    :param film_id: film uuid
    :param film_service: film service
    :param token: authorization token
    :param authorize: JWT token
    :returns: Information about film
    """

    try:
        authorize.jwt_required()
    except JWTDecodeError:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail=error_msgs.non_valid_token)
    except MissingTokenError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail=error_msgs.authorized_only)

    roles = authorize.get_raw_jwt()['roles']
    film = await film_service.get_film_by_id(film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.film_not_found)

    if film.tag == 'subscription_only' and not ('subscriber' in roles):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                            detail=error_msgs.subscription_only)

    return DetailFilmApi(uuid=film.id,
                         title=film.title,
                         imdb_rating=film.imdb_rating,
                         price=film.price,
                         description=film.description,
                         genre=film.genre,
                         actors=film.actors,
                         writers=film.writers,
                         director=film.director,
                         tag=film.tag,
                         )
