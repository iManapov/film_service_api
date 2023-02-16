import uuid

from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from src.services.genre import GenreService, get_genre_service
from src.models.genre import BaseGenreApi, DetailGenreApi
from src.core.params import params
from src.core.error_messages import error_msgs


router = APIRouter()


@router.get('/',
            response_model=list[BaseGenreApi],
            summary="Information about a few genres",
            description="Short information about a few genres",
            )
async def get_genres(
        sort: Optional[str] = params.sort,
        limit: Optional[int] = params.limit,
        page: Optional[int] = params.page,
        genre_service: GenreService = Depends(get_genre_service)
) -> Optional[list[BaseGenreApi]]:
    """
    Returns information about a few genres

    :param sort: sorting field
    :param limit: the number of films on one page
    :param page: page number
    :param genre_service: genre service
    :return: information about a few genres
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
            summary="Detailed information about genre",
            description="Detailed information about genre",
            )
async def genre_details(
        genre_id: uuid.UUID = params.genre_id,
        genre_service: GenreService = Depends(get_genre_service)
) -> DetailGenreApi:
    """
    Returns detailed information about genre

    :param genre_id: genre uuid
    :param genre_service: genre service
    :return: detailed information about genre
    """

    genre = await genre_service.get_genre_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=error_msgs.genre_not_found)
    return DetailGenreApi(uuid=genre.id, name=genre.name, description=genre.description)
