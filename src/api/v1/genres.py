import uuid

from http import HTTPStatus
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException

from services.genre import GenreService, get_genre_service
from models.genre import BaseGenreApi, DetailGenreApi
from core.params import params
from core.error_messages import error_msgs


router = APIRouter()


@router.get('/',
            response_model=list[BaseGenreApi],
            summary="Информация по нескольким жанрам",
            description="Краткая информация по нескольким жанрам",
            )
async def genres(
        sort: Union[str, None] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        genre_service: GenreService = Depends(get_genre_service)
) -> Union[list[BaseGenreApi], None]:
    """
    Возвращает информацию по нескольким жанрам

    @param sort: имя поля по которому идет сортировка
    @param limit: количество записей на странице
    @param page: номер страницы
    @param genre_service:
    @return: Данные по жанрам
    """

    genres, errors = await genre_service.get_genres(sort=sort, limit=limit, page=page)

    if errors:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail=error_msgs.bad_request)

    non_detail_genre_list = [
        BaseGenreApi(uuid=genre['_source']['id'],
                     name=genre['_source']['name']
                     )
        for genre in genres
    ]

    return non_detail_genre_list


@router.get('/{genre_id}',
            response_model=DetailGenreApi,
            summary="Информация по одному жанру",
            description="Детальная информация по отдельному жанру",
            )
async def genre_details(
        genre_id: uuid.UUID = params.genre_id,
        genre_service: GenreService = Depends(get_genre_service)
) -> DetailGenreApi:
    """Возвращает информацию по одному жанру."""

    genre = await genre_service.get_genre_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.genre_not_found)
    return DetailGenreApi(uuid=genre.id, name=genre.name, description=genre.description)
