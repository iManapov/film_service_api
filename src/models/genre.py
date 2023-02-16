import uuid

from typing import Optional
from pydantic import BaseModel

from src.models.mixin import JsonMixin


class Genre(JsonMixin):
    """Genre model in ES"""

    id: uuid.UUID
    name: str
    description: Optional[str]


class BaseGenreApi(BaseModel):
    """API-model for short genre description"""

    uuid: uuid.UUID
    name: str


class DetailGenreApi(BaseGenreApi):
    """API-model for detailed genre description"""

    description: Optional[str]
