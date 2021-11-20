import redis

class RedisClient:
    _client = None
    def __init__(self, host='redis', port=6379, db=0):
        # connect to redis
        # TODO: Use env configured vars.
        self._client = redis.StrictRedis(host=host, port=port, db=db)
 
    def getClient(self):
        return self._client
