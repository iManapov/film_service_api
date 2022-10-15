import os
import sys
import time

from redis import Redis, exceptions

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from settings import test_settings


if __name__ == '__main__':
    while True:
        try:
            redis_client = Redis(host=test_settings.redis_host, port=test_settings.redis_port, socket_connect_timeout=1)
            if redis_client.ping():
                break
        except exceptions.ConnectionError:
            pass
        time.sleep(3)
