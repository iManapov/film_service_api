import uuid

from typing import Optional
from pydantic import BaseModel

from src.models.mixin import JsonMixin


class Genre(JsonMixin):
    """Модель жанра в ES."""

    id: uuid.UUID
    name: str
    description: Optional[str]


class BaseGenreApi(BaseModel):
    """API-Модель для краткого описания жанра."""

    uuid: uuid.UUID
    name: str


class DetailGenreApi(BaseGenreApi):
    """API-Модель для подробного описания жанра."""

    description: Optional[str]
