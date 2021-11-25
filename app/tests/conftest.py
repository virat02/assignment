import pytest, os
from package.redis.client import RedisClient
from routes.routes import proxy_app

@pytest.fixture(scope="session")
def create_app():
    return proxy_app

@pytest.fixture(scope="session")
def client(create_app):
    return proxy_app.test_client()

@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    host = os.getenv('BACKING_REDIS_HOST')
    port = os.getenv('BACKING_REDIS_PORT')
    redisClient = RedisClient(host=host, port=port, db=0)

    redisClient.put('color', 'blue')
    redisClient.put('test', 'test')
    redisClient.put('test1', 'test1')
    redisClient.put('test2', 'test2')
    redisClient.put('test3', 'test3')
    redisClient.put('test4', 'test4')