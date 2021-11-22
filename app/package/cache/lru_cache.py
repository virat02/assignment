from collections import OrderedDict
 
class LRUCache:

    def __init__(self, capacity: int):
        # Stores keys in the order of least recently used to most recently used.
        self.cache = OrderedDict()
        self.capacity = capacity
        # TODO: Add global expiry.
 
    # 1. Return -1 if key not found.
    # 2. Return value if key found and also mark it as most recently used.
    def get(self, key):
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]
 
    # 1. Add key-val to the cache
    # 2. Mark the key as most recently used.
    # 3. If cache is over-capacity, remove the least recently used key.
    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            # Pop in FIFO order since LRU key is at the top
            self.cache.popitem(last = False)