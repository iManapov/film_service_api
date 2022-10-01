import uuid

from typing import Optional

from models.mixin import JsonMixin


class Genre(JsonMixin):
    id: uuid.UUID
    name: str
