import uuid

from typing import Optional
from pydantic import BaseModel

from src.models.mixin import JsonMixin


class Person(JsonMixin):
    """Person model in ES"""

    id: uuid.UUID
    name: str
    role: Optional[list[str]]
    film_ids: Optional[list[uuid.UUID]]


class BasePersonApi(BaseModel):
    """API-model for person description"""

    uuid: uuid.UUID
    name: str
    role: Optional[list[str]]
    film_ids: Optional[list[uuid.UUID]]
