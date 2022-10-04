import time

from elasticsearch import Elasticsearch

from functional import settings

if __name__ == '__main__':
    es_client = Elasticsearch(
        hosts=f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}',
        validate_cert=False,
        use_ssl=False
    )
    while True:
        if es_client.ping():
            break
        time.sleep(1)