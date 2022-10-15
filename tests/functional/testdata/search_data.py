search_test_data = [
    (
        '/api/v1/films/search',
        {"page[number]": -4, "page[size]": 20},
        {"status": 422, "length": 0}
    ),
    (
        '/api/v1/films/search',
        {"page[number]": 2, "page[size]": 101},
        {"status": 422, "length": 0}),
    (
        '/api/v1/films/search',
        {"page[number]": 1},
        {"status": 422, "length": 0},
    ),
    (
        '/api/v1/films/search',
        {"query": "The Man"},
        {"status": 200, "length": 1},
    ),
    (
        '/api/v1/films/search',
        {"query": "The Star", "page[number]": 1, "page[size]": 45},
        {"status": 200, "length": 45},
    ),
    (
        '/api/v1/films/search',
        {"query": "The Star"},
        {"status": 200, "length": 50}
    ),
    (
        '/api/v1/persons/search',
        {'query': 'Eduardo Durant'},
        {'status': 200, 'length': 30}
    ),
    (
        '/api/v1/persons/search',
        {'query': 'Mashed potato'},
        {'status': 200, 'length': 0}
    ),
    (
        '/api/v1/persons/search',
        {'query': 'Eduardo Durant', 'page[size]': 60, "page[number]": -1},
        {'status': 422}
    ),
]
