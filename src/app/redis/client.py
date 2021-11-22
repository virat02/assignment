import redis

class RedisClient:
    _redis = None

    def __init__(self, host='redis', port=6379, db=0):
        # connect to redis
        # TODO: Use env configured vars.
        self._redis = redis.StrictRedis(host=host, port=port, db=db)

    def getVal(self, key):
        try:
            val = self._redis.get(key)
            return val if val else f'Key: {key} not found!'
        except e:
            return (
                f'Error getting Key: {key}.\n' 
                f'Error: {e}'
            )
    
    def setKeyVal(self, key, val):
        try:
            self._redis.set(key, val)
        except e:
            return (
                f'Error setting key: {key} with val: {val}.\n'
                f'Error: {e}'
            )