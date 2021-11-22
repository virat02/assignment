from flask import Flask
from redisclient.redis_client import RedisClient

# Initialize RedisClient
redisClient = RedisClient()
client = redisClient.getClient()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

client.set('1', 'test-value-1')

@app.route('/get/<key>')
def get(key):
    return client.get(key)
