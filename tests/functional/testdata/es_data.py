import uuid


es_data = [{
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