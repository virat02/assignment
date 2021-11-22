from package.redis.client import RedisClient
from package.cache.lru_cache import LRUCache

class Proxy:

    def __init__(self):
        # Initialize RedisClient
        self.redisClient = RedisClient()

        # Initialize LRU Cache
        self.cache = LRUCache(4)

    def get(self, key):
        val = self.cache.get(key)

        if val != -1:
            return val
        else:
            val = self.redisClient.getVal(key)
            if val:
                self.cache.put(key, val) 

            return val
    
    def put(self, key, val):
        return self.redisClient.put(key, val)

