import os
import sys
import time

from elasticsearch import Elasticsearch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from settings import test_settings


if __name__ == '__main__':
    es_client = Elasticsearch(hosts=f'{test_settings.elastic_host}:{test_settings.elastic_port}',
                              validate_cert=False, use_ssl=False)
    while True:
        if es_client.ping():
            break
        time.sleep(3)
