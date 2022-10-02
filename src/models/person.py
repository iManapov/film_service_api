import uuid

from typing import Optional
from pydantic import BaseModel

from models.mixin import JsonMixin


class Person(JsonMixin):
    """Модель персоналий в ES."""

    id: uuid.UUID
    name: str
    role: Optional[list[str]]
    film_ids: Optional[list[uuid.UUID]]


class BasePersonApi(BaseModel):
    """API-Модель для описания персоналий."""

    uuid: uuid.UUID
    name: str
    role: Optional[list[str]]
    film_ids: Optional[list[uuid.UUID]]
