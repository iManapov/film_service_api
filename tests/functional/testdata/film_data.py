import datetime
from http import HTTPStatus
import uuid


es_film_data = [
    {
        "id": str(uuid.uuid4()),
        "imdb_rating": 8.5,
        "genre": [
            {"id": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure"},
            {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
        ],
        "title": "The Star",
        "creation_date": datetime.datetime.now().isoformat(),
        "description": "New World",
        "director": ["Stan"],
        "actors_names": ["Ann", "Bob"],
        "writers_names": ["Ben", "Howard"],
        "actors": [
            {"id": "26e83050-29ef-4163-a99d-b546cac208f8", "name": "Ann"},
            {"id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1", "name": "Bob"},
        ],
        "writers": [
            {"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "Ben"},
            {"id": "26e83050-29ef-4163-a99d-b546cac208f8", "name": "Howard"},
        ],
    }
    for _ in range(59)
]

es_film_data.append(
    {
        "id": "59a067af-b255-4464-839f-daad80dd78d1",
        "imdb_rating": 8.5,
        "genre": [
            {"id": "120a21cf-9097-479e-904a-13dd7198c1de", "name": "Romance"},
            {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
        ],
        "title": "The Man",
        "creation_date": datetime.datetime.now().isoformat(),
        "description": "New World",
        "director": ["Stan"],
        "actors_names": ["Ann", "Bob"],
        "writers_names": ["Ben", "Howard"],
        "actors": [
            {"id": "26e83050-29ef-4163-a99d-b546cac208f8", "name": "Ann"},
            {"id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1", "name": "Bob"},
        ],
        "writers": [
            {"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "Ben"},
            {"id": "26e83050-29ef-4163-a99d-b546cac208f8", "name": "Howard"},
        ],
    }
)

one_film_test_data = [
    (12345, {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "response": ""}),
    ("string", {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "response": ""}),
    (
        "59a067af-b255-4464-839f-daad80dd78d1",  # Действительный
        {
            "status": HTTPStatus.OK,
            "response": {
                "uuid": "59a067af-b255-4464-839f-daad80dd78d1",
                "title": "The Man",
                "imdb_rating": 8.5,
                "description": "New World",
                "genre": [
                    {"id": "120a21cf-9097-479e-904a-13dd7198c1de", "name": "Romance"},
                    {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
                ],
                "actors": [
                    {
                        "id": "26e83050-29ef-4163-a99d-b546cac208f8",
                        "name": "Ann",
                        "role": None,
                        "film_ids": None,
                    },
                    {
                        "id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1",
                        "name": "Bob",
                        "role": None,
                        "film_ids": None,
                    },
                ],
                "writers": [
                    {
                        "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
                        "name": "Ben",
                        "role": None,
                        "film_ids": None,
                    },
                    {
                        "id": "26e83050-29ef-4163-a99d-b546cac208f8",
                        "name": "Howard",
                        "role": None,
                        "film_ids": None,
                    },
                ],
                "director": ["Stan"],
            },
        },
    ),
    (
        "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",  # Недействительный
        {"status": HTTPStatus.NOT_FOUND, "response": ""},
    ),
]

list_film_test_data = [
    ({"page[number]": -4, "page[size]": 20}, {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "length": 0}),
    ({"page[number]": 2, "page[size]": 101}, {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "length": 0}),
    ({"page[number]": 1, "page[size]": 45}, {"status": HTTPStatus.OK, "length": 45}),
    ({"page[number]": 10, "sort": "-imdb_rating"}, {"status": HTTPStatus.OK, "length": 0}),
    (
        {"page[number]": 1, "genre": "120a21cf-9097-479e-904a-13dd7198c1de"},
        {"status": HTTPStatus.OK, "length": 1},
    ),
]
