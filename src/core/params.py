from dataclasses import dataclass

from fastapi import Query, Path
from pydantic import Required


@dataclass
class Params:
    """
    Класс параметров запроса API
    """
    sort: Query = Query(
        default=None,
        title="Параметры, по которым осуществляется сортировка"
    )

    limit: Query = Query(
        default=50,
        title="Размер страницы",
        alias="page[size]",
        ge=1,
        le=100
    )

    page: Query = Query(
        default=1,
        title="Номер страницы",
        alias="page[number]",
        ge=1
    )

    query: Query = Query(
        default=Required,
        title="Поисковый запрос"
    )

    film_id: Path = Path(
        default=Required,
        title="UUID фильма"
    )

    genre: Query = Query(
        default=None,
        title="UUID жанра для фильтрации фильмов"
    )

    person_id: Path = Path(
        default=Required,
        title="UUID персоны"
    )

    genre_id: Path = Path(
        default=Required,
        title="UUID жанра"
    )

params = Params()