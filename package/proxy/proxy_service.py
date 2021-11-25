import os
from package.redis.client import RedisClient
from package.cache.lru_cache import LRUCache
from package.proxy.resp_parser import RespParser

class Proxy:

    def __init__(self, is_tcp=False):
        # Initialize RedisClient
        host = os.getenv('BACKING_REDIS_HOST')
        port = os.getenv('BACKING_REDIS_PORT')

        print(f'Getting redis client from host: {host}, port: {port}')
        self._redisClient = RedisClient(host=host, port=port, db=0)

        # Initialize LRU Cache
        self._cache = LRUCache(os.getenv('CACHE_CAPACITY'), os.getenv('CACHE_GLOBAL_EXPIRY'))
        self._is_tcp = is_tcp

        if self._is_tcp:
            self._resp_parser = RespParser()

    def get(self, key):
        if self._is_tcp:
            key = self._resp_parser.decode(key)
            print(f'Decoded key: {key}')
        
        val = self._cache.get(key)

        if val != -1:
            print('got from cache')
            return val
        else:
            val = self._redisClient.getVal(key)

            if val != -1:
                print(f'Added {key} to cache')
                self._cache.put(key, val) 
            else:
                print('Key not found in redis either')

            print(f'got from redis {val}')
            return val
    
    def put(self, key, val):
        if self._is_tcp:
            key = self._resp_parser.decode(key)
            val = self._resp_parser.decode(val)

        return self._redisClient.put(key, val)

