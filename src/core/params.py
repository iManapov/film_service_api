from dataclasses import dataclass

from fastapi import Query, Path
from pydantic import Required


@dataclass
class Params:
    """API request parameters class"""

    sort: Query = Query(
        default=None,
        title="Sorting parameter"
    )

    limit: Query = Query(
        default=50,
        title="Page size",
        alias="page[size]",
        ge=1,
        le=100
    )

    page: Query = Query(
        default=1,
        title="Page number",
        alias="page[number]",
        ge=1
    )

    query: Query = Query(
        default=Required,
        title="Search query"
    )

    film_id: Path = Path(
        default=Required,
        title="Film UUID"
    )

    genre: Query = Query(
        default=None,
        title="Genre UUID to filter for"
    )

    person_id: Path = Path(
        default=Required,
        title="Person UUID"
    )

    genre_id: Path = Path(
        default=Required,
        title="Genre UUID"
    )


params = Params()
