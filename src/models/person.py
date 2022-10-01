import uuid

from typing import Optional

from models.mixin import JsonMixin


class Persons(JsonMixin):
    id: uuid.UUID
    name: str
