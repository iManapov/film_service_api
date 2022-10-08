import uuid

from typing import Optional
from pydantic import BaseModel

from src.models.mixin import JsonMixin
from src.models.person import Person


class Film(JsonMixin):
    """
    Модель фильма в ES
    """
    id: uuid.UUID
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: Optional[list]
    actors: Optional[list[Person]]
    writers: Optional[list[Person]]
    director: Optional[list]


# Модели ответа API
class BaseFilmApi(BaseModel):
    """
    API-Модель для краткого описания фильма
    """
    uuid: uuid.UUID
    title: str
    imdb_rating: Optional[float]


class DetailFilmApi(BaseFilmApi):
    """
    API-Модель для подробного описания фильма
    """
    description: Optional[str]
    genre: Optional[list]
    actors: Optional[list]
    writers: Optional[list]
    director: Optional[list]
