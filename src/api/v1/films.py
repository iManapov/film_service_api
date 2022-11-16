import uuid

from http import HTTPStatus
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError, MissingTokenError

from src.services.film import FilmService, get_film_service
from src.models.film import BaseFilmApi, DetailFilmApi
from src.core.params import params
from src.core.error_messages import error_msgs

# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get('/search',
            response_model=list[BaseFilmApi],
            summary="Поиск по фильмам",
            description="Осуществляет нечеткий поиск по фильмам",
            )
async def films(
        sort: Union[str, None] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        query: Optional[str] = params.query,
        film_service: FilmService = Depends(get_film_service)
) -> Union[list[BaseFilmApi], None]:
    """
    Возвращает результаты поиска по названию фильма

    @param sort: имя поля по которому идет сортировка
    @param limit: количество записей на странице
    @param page: номер страницы
    @param query: поисковый запрос
    @param film_service:
    @return: Данные по фильмам
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
            summary="Похожие фильмы",
            description="Похожие фильмы для заданного фильма",
            )
async def same_films(
        film_id: uuid.UUID = params.film_id,
        sort: Union[str, None] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        film_service: FilmService = Depends(get_film_service)
) -> Union[list[BaseFilmApi], None]:
    """
    Возвращает похожие фильмы для заданного фильма

    @param film_id: uuid фильма
    @param sort: имя поля по которому идет сортировка
    @param limit: количество записей на странице
    @param page: номер страницы
    @param film_service:
    @return: Данные по похожим фильмам
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
            summary="Информация по нескольким фильмам",
            description="Краткая информация по нескольким фильмам",
            )
async def films(
        sort: Union[str, None] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        genre: Optional[Union[list[uuid.UUID]]] = params.genre,
        film_service: FilmService = Depends(get_film_service)
) -> Union[list[BaseFilmApi], None]:
    """
    Возвращает информацию по нескольким фильмам

    @param sort: имя поля по которому идет сортировка
    @param limit: количество записей на странице
    @param page: номер страницы
    @param genre: uuid-жанра для фильтрации
    @param film_service:
    @return: Данные по фильмам
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
                    imdb_rating=film['_source']['imdb_rating']
                    )
        for film in films
    ]

    return non_detail_film_list


@router.get('/{film_id}',
            response_model=DetailFilmApi,
            summary="Информация по одному фильму",
            description="""
                        Детальная информация по отдельному фильму.
                        Если у фильма проставлен тэг 'subscription_only'
                        то доступ только пользователям с ролью 'subscriber
                        """
            )
async def film_details(
        film_id: uuid.UUID = params.film_id,
        film_service: FilmService = Depends(get_film_service),
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(bearerFormat='Bearer')),
        authorize: AuthJWT = Depends()) -> DetailFilmApi:
    """
    Возвращает информацию по одному фильму
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
                         description=film.description,
                         genre=film.genre,
                         actors=film.actors,
                         writers=film.writers,
                         director=film.director
                         )