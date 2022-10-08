import time

from redis import Redis, exceptions
from tests.functional.settings import test_settings


if __name__ == '__main__':
    while True:
        try:
            redis_client = Redis(host=test_settings.redis_host, port=test_settings.redis_port, socket_connect_timeout=1)
            if redis_client.ping():
                break
        except exceptions.ConnectionError:
            print('Cannot connect to Redis')
        time.sleep(1)
