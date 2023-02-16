import uuid

from typing import Optional
from pydantic import BaseModel

from src.models.mixin import JsonMixin
from src.models.person import Person


class Film(JsonMixin):
    """Film model in ES"""

    id: uuid.UUID
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: Optional[list]
    actors: Optional[list[Person]]
    writers: Optional[list[Person]]
    director: Optional[list]
    tag: Optional[str]
    price: float


class BaseFilmApi(BaseModel):
    """API-model for short film description"""

    uuid: uuid.UUID
    title: str
    imdb_rating: Optional[float]
    price: float
    tag: Optional[str]


class DetailFilmApi(BaseFilmApi):
    """API-model for detailed film description"""

    description: Optional[str]
    genre: Optional[list]
    actors: Optional[list]
    writers: Optional[list]
    director: Optional[list]
