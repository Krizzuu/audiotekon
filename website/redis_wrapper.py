import redis.exceptions
from redis.client import Redis


class RedisWrapper:
    def __init__(self):
        self.client = Redis(host="redis", port=6379, db=0, socket_connect_timeout=2, socket_timeout=2, decode_responses=True)

    def set(self, key, value):
        try:
            self.client.set(key, value)
        except redis.exceptions.ConnectionError as e:
            pass

    def get(self, key):
        try:
            return self.client.get(key)
        except redis.exceptions.ConnectionError as e:
            return None