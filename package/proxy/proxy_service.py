import os
from package.redis.client import RedisClient
from package.cache.lru_cache import LRUCache
from package.proxy.resp_parser import RespParser

class Proxy:

    def __init__(self, is_tcp: bool = False, debug: bool = False) -> None:
        self._debug = debug

        # Initialize RedisClient
        host = os.getenv('BACKING_REDIS_HOST')
        port = os.getenv('BACKING_REDIS_PORT')

        if self._debug:
            print(f'Getting redis client from host: {host}, port: {port}')

        self._redisClient = RedisClient(host=host, port=port, db=0)

        # Initialize LRU Cache
        self._cache = LRUCache(os.getenv('CACHE_CAPACITY'), os.getenv('CACHE_GLOBAL_EXPIRY'), self._debug)
        self._is_tcp = is_tcp

        if self._is_tcp:
            self._resp_parser = RespParser()

    def get(self, key: str) -> str:
        """
        1. Returns value for key from cache if key exists in cache.
        2. Returns value for key from backing redis if key does not exist in cache
        3. Returns "{key} not found" if the key is not found neither in cache or backing redis.
        NOTE: For a TCP proxy, resp parser will parse the requested key before further implementation.
        """
        if self._is_tcp:
            key = self._resp_parser.decode(key)
            if self._debug:
                print(f'Decoded key: {key}')

            if key == 'Invalid':
                return 'Invalid key requested'

            key = key[1]
        
        # Try fetching value for key from cache
        val = self._cache.get(key)

        # key found in cache
        if val != -1:
            if self._debug:
                print('got from cache')

            return val
        else:
            # Try fetching value for key from backing redis
            val = self._redisClient.getVal(key)

            # key found in backing redis
            if val != -1:
                # Add (key, val) to cache to serve from cache next time
                self._cache.put(key, val)

                if self._debug:
                    print(f'Added {key} to cache')
            elif self._debug:
                print('Key not found in redis either')

            if self._debug:
                print(f'got from redis {val}')

            return val if val != -1 else f'{key} not found!'

