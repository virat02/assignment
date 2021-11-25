import socket, sys, os, pytest
from package.redis.client import RedisClient

@pytest.fixture()
def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("socket creation failed with error %s" %(err))

    try:
        host = os.getenv('PROXY_HOST')
        port = os.getenv('PROXY_PORT')
    except socket.gaierror:
        print("there was an error resolving the host")
        sys.exit()

    # connecting to the server
    s.connect((host, int(port)))
    return s

@pytest.fixture(scope="session")
def setup_test_data():
    host = os.getenv('BACKING_REDIS_HOST')
    port = os.getenv('BACKING_REDIS_PORT')
    redisClient = RedisClient(host=host, port=port, db=0)

    redisClient.put('foo', 'bar')
    redisClient.put('foo1', 'bar1')
    redisClient.put('foo2', 'bar2')
    redisClient.put('foo3', 'bar3')
    redisClient.put('foo4', 'bar4')
    redisClient.put('foo5', 'bar5')