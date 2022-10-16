import os
import sys

from elasticsearch import Elasticsearch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from settings import test_settings
from backoff import backoff


@backoff(test_settings.backoff_start_sleep_time,
         test_settings.backoff_factor,
         test_settings.backoff_border_sleep_time)
def connect_to_es(host: str, port: int) -> Elasticsearch:
    """
    Инициализация подключения к elasticsearch.

    :param host: хост elasticsearch
    :param port: порт elasticsearch
    :return: подключение к elasticsearch
    """
    return Elasticsearch(hosts=f'{host}:{port}', validate_cert=False, use_ssl=False)


if __name__ == '__main__':
    connect_to_es(test_settings.elastic_host, test_settings.elastic_port)
