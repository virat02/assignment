import os
from package.redis.client import RedisClient
from package.cache.lru_cache import LRUCache
from package.proxy.resp_parser import RespParser

class Proxy:

    def __init__(self, is_tcp: bool = False, debug: bool = False, cache_capacity: int = 5, cache_expiry: int = 60000) -> None:
        self._debug = debug

        # Initialize RedisClient
        host = os.getenv('BACKING_REDIS_HOST')
        port = os.getenv('BACKING_REDIS_PORT')

        if self._debug:
            print(f'Getting redis client from host: {host}, port: {port}')

        self._redisClient = RedisClient(host=host, port=port, db=0)

        # Initialize LRU Cache
        # NOTE: Priority given to cache environment variables
        self._cache_capacity = os.getenv('CACHE_CAPACITY') or cache_capacity
        self._cache_expiry = os.getenv('CACHE_GLOBAL_EXPIRY') or cache_expiry

        self._cache = LRUCache(self._cache_capacity, self._cache_expiry, self._debug)
        self._is_tcp = is_tcp

        if self._is_tcp:
            self._resp_parser = RespParser()

    def get(self, key: str) -> str:
        """
        1. Returns value for key from cache if key exists in cache.
        2. Returns value for key from backing redis if key does not exist in cache
        3. Returns "{key} not found" if the key is not found neither in cache or backing redis.
        NOTE: For a TCP proxy, resp parser will encode and decode in RESP format.
        """
        if self._is_tcp:
            key = self._resp_parser.decode(key)
            if self._debug:
                print(f'Decoded key: {key}')

            if key == 'Invalid':
                return self._resp_parser.encodeError('Invalid key requested') 
            elif key[0].lower() != 'get':
                return self._resp_parser.encodeError('Not a GET request') 

            # Fetch the 'key' from the RESP GET request
            key = key[1]
        
        # Try fetching value for key from cache
        val = self._cache.get(key)

        # key found in cache
        if val != -1:
            if self._debug:
                print('got from cache')

            return val if not self._is_tcp else self._resp_parser.encodeString(val)
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

            if not self._is_tcp:
                return val if val != -1 else f'{key} not found!'
            else:
                if val == -1:
                    return self._resp_parser.encodeError(f'{key} not found!')
                else:
                    return self._resp_parser.encodeString(val)

