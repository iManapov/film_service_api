import uuid

correct_id = 'c9686044-6a5c-4c0f-aa71-3bc485d88ac4'

es_data_persons = [{
    'id': str(uuid.uuid4()),
    'name': 'Eduardo Durant',
    'role': ['actor'],
    'film_ids': [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
} for _ in range(29)]
es_data_persons.append({
    'id': correct_id,
    'name': 'Eduardo Durant',
    'role': ['actor'],
    'film_ids': [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
})
