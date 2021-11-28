import time, sys
from collections import OrderedDict
from typing import Union
class LRUCache:

    def __init__(self, capacity: int = sys.maxsize, expiry: int = 300000, debug: bool = False) -> None:
        self._debug = debug

        # Stores keys in the order of least recently used to most recently used.
        self._cache = OrderedDict()

        # Set cache fixed key size
        self._capacity = capacity

        # Set cache global expiry (milliseconds)
        # NOTE: If expiry is max int, cache would never expire.
        self._expiry = expiry
 

    def get(self, key: str) -> Union[int, str]:
        """
        1. Return -1 if key not found.
        2. Return -1 if requested key has expired (Treat it as key not found)
        3. Return value if key found and also mark it as most recently used.
        """
        if key not in self._cache:
            return -1
        else:
            (val, expiry_time) = self._cache[key]

            # If key has expired
            if self.isExpired(expiry_time):
                if self._debug:
                    print(f'{key} expired, removing from cache.')

                # Remove from local cache
                self._cache.pop(key, -1)

                return -1

            self._cache.move_to_end(key)
            return val
 

    def put(self, key: str, value: str) -> None:
        """
        1. Add key: (value, expiry_time) to the cache
        2. Mark the key as most recently used.
        3. If cache is over-capacity, remove the least recently used key.
        """
        time_now = int(time.time() * 1000)
        self._cache[key] = (value, time_now + self._expiry)

        self._cache.move_to_end(key)

        if len(self._cache) > self._capacity:
            # Pop in FIFO order since LRU key is at the top
            val = self._cache.popitem(last = False)

            if self._debug:
                print(f'over-capacity, removing {val} from cache.')
    

    def isExpired(self, expiry_time: int) -> bool:
        """Returns True if time now is greater than the cache expiry time set else returns False"""
        time_now = int(time.time() * 1000)
        
        if self._debug:
            print(f'time_now: {time_now}.')
            print(f'expiry_time: {expiry_time}.')
        return time_now > expiry_time
