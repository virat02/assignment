from lru_cache import LRUCache

class CacheClient:
    _cache = None

    def __init__(self, capacity: int):
        # TODO: Use env configured vars for cache capacity
        self._cache = LRUCache(4)