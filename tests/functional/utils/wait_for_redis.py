import os
import sys

from redis import Redis

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from settings import test_settings
from backoff import backoff


@backoff(test_settings.backoff_start_sleep_time,
         test_settings.backoff_factor,
         test_settings.backoff_border_sleep_time)
def connect_to_redis(host: str, port: int) -> Redis:
    """
    Инициализация подключения к Redis.

    :param host: хост Redis
    :param port: порт Redis
    :return: подключение к Redis
    """
    return Redis(host=host, port=port, socket_connect_timeout=1)


if __name__ == '__main__':
    client = connect_to_redis(host=test_settings.redis_host, port=test_settings.redis_port)
