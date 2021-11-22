import os
from flask import Flask, request
from package.proxy.proxy_service import Proxy

# Initialize Proxy
proxy = Proxy()

# set test data for the time being.
proxy.put('color', 'blue')
proxy.put('test', 'test-output')

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

@app.route('/get/<key>')
def get(key):
    return proxy.get(key)

if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'))