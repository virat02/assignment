import os
from package.redis.client import RedisClient
from package.cache.lru_cache import LRUCache

class Proxy:

    def __init__(self):
        # Initialize RedisClient
        redis_address = os.getenv('BACKING_REDIS_ADDRESS')
        [host, port] = redis_address.split(":")

        self._redisClient = RedisClient(host=host, port=port)

        # Initialize LRU Cache
        self._cache = LRUCache(os.getenv('CACHE_CAPACITY'), os.getenv('CACHE_GLOBAL_EXPIRY'))

    def get(self, key):
        val = self._cache.get(key)

        if val != -1:
            print('got from cache')
            return val
        else:
            val = self._redisClient.getVal(key)
            if val:
                print(f'Added {key} to cache')
                self._cache.put(key, val) 

            print('got from redis')
            return val
    
    def put(self, key, val):
        return self._redisClient.put(key, val)

