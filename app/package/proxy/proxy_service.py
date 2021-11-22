from package.redis.client import RedisClient
from package.cache.lru_cache import LRUCache

class Proxy:

    def __init__(self):
        # Initialize RedisClient
        self._redisClient = RedisClient()

        # Initialize LRU Cache
        self._cache = LRUCache(4)

    def get(self, key):
        val = self._cache.get(key)

        if val != -1:
            return val
        else:
            val = self._redisClient.getVal(key)
            if val:
                self._cache.put(key, val) 

            return val
    
    def put(self, key, val):
        return self._redisClient.put(key, val)

