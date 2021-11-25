from typing import Union
from redis import Redis

class RedisClient:
    _redis = None

    def __init__(
        self, 
        host: str = 'redis-container', 
        port: int = 6379, 
        db: int = 0, 
        debug: bool = False
    ) -> None:
        self._debug = debug

        # connect to backing redis
        try:
            self._redis = Redis(host=host, port=port, db=db, decode_responses=True)
        except:
            if self._debug:
                print(f'Could not connect to redis; host: ${host} on port ${port}')

    def getVal(self, key: str) -> Union[int, str]:
        """
        1. Returns value for key from backing redis.
        2. Returns -1 if key not found in backing redis.
        3. Returns an error string for any exception occurred while 
           fetching value for key from backing redis.
        """
        try:
            val = self._redis.get(key)
            return val if val else -1
        except:
            return f'Error getting Key: {key}.'
    
    def put(self, key: str, val: str) -> Union[None, str]:
        """
        1. Sets the value for key in backing redis.
        2. Returns an error string for any exception occurred while
           setting value for key in backing redis.
        """
        try:
            self._redis.set(key, val)
        except:
            return f'Error setting key: {key} with val: {val}.'