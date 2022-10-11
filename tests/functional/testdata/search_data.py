search_test_data = [
    (
        {
            'page[number]': -4,
            'page[size]': 20
        },
        {
            'status': 422,
            'length': 0
         }
    ),
    (
        {
            'page[number]': 2,
            'page[size]': 101
        },
        {
            'status': 422,
            'length': 0
        }
    ),
    (
        {
            'page[number]': 1,
        },
        {
            'status': 422,
            'length': 0
        }
    ),
    (
        {
            'query': 'The Man',
        },
        {
            'status': 200,
            'length': 1
        }
    ),
    (
        {
            'query': 'The Star',
            'page[number]': 1,
            'page[size]': 45
        },
        {
            'status': 200,
            'length': 45
        }
    ),
    (
        {
            'query': 'The Star'
        },
        {
            'status': 200,
            'length': 50
        }
    )
]