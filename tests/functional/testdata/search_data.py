from http import HTTPStatus


search_test_data = [
    (
        '/api/v1/films/search',
        {"page[number]": -4, "page[size]": 20},
        {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "length": 0}
    ),
    (
        '/api/v1/films/search',
        {"page[number]": 2, "page[size]": 101},
        {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "length": 0}),
    (
        '/api/v1/films/search',
        {"page[number]": 1},
        {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "length": 0},
    ),
    (
        '/api/v1/films/search',
        {"query": "The Man"},
        {"status": HTTPStatus.OK, "length": 1},
    ),
    (
        '/api/v1/films/search',
        {"query": "The Star", "page[number]": 1, "page[size]": 45},
        {"status": HTTPStatus.OK, "length": 45},
    ),
    (
        '/api/v1/films/search',
        {"query": "The Star"},
        {"status": HTTPStatus.OK, "length": 50}
    ),
    (
        '/api/v1/persons/search',
        {'query': 'Eduardo Durant'},
        {'status': HTTPStatus.OK, 'length': 30}
    ),
    (
        '/api/v1/persons/search',
        {'query': 'Mashed potato'},
        {'status': HTTPStatus.OK, 'length': 0}
    ),
    (
        '/api/v1/persons/search',
        {'query': 'Eduardo Durant', 'page[size]': 60, "page[number]": -1},
        {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
    ),
]