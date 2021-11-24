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
            return val if val else -1
        except:
            return f'Error getting Key: {key}.\n'
    
    def put(self, key, val):
        try:
            self._redis.set(key, val)
        except:
            return f'Error setting key: {key} with val: {val}.\n'