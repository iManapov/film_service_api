import uuid
from random import choice

es_genre_data = [
    {
        "id": str(uuid.uuid4()),
        "name": choice(
            [
                "Action",
                "Sci-Fi",
                "Adventure",
                "Fantasy",
                "Drama",
                "Music",
                "Romance",
                "Thriller",
            ]
        ),
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
    }
    for _ in range(60)
]
