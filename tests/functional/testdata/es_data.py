import uuid
from random import choice


movies_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': [{'id': str(uuid.uuid4()), 'name': 'Action'},
                  {'id': str(uuid.uuid4()), 'name': 'Sci-Fi'}],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ]
    } for _ in range(60)]

genres_data = [{
    'id': str(uuid.uuid4()),
    'name': choice(['Action', 'Sci-Fi', 'Adventure', 'Fantasy', 'Drama', 'Music', 'Romance', 'Thriller']),
    'description': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
    } for _ in range(60)]
