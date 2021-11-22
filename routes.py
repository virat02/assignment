from flask import Flask
from redisclient.redis_client import RedisClient

# Initialize RedisClient
redisClient = RedisClient()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

@app.route('/get/<key>')
def get(key):
    return redisClient.getVal(key)

@app.route('/set/<key>/<val>', methods=['POST'])
def setKeyVal(key, val):
    return redisClient.setKeyVal(key, val)