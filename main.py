from redisclient.redis_client import RedisClient

if __name__ == "__main__":
    print('Inside main, establishing Redis connection.')

    # Initialize RedisClient
    redisClient = RedisClient()
    client = redisClient.getClient()

    print('Got client: ', client)

    client.set('1', 'hello')

    result = client.get('1')

    print('I am working!')
    print('Result: ', result)