from redis import Redis

class RedisClient:
    _redis = None

    def __init__(self, host='redis', port=6379, db=0):
        # connect to redis
        try:
            self._redis = Redis(host=host, port=port, db=db, decode_responses=True)
        except:
            print(f'Could not connect to redis; host: ${host} on port ${port}')

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