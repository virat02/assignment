from flask import Flask
from package.proxy.proxy_service import Proxy

# Initialize Proxy
proxy = Proxy(is_tcp=False)

# set test data for the time being.
proxy.put('color', 'blue')
proxy.put('test', 'test')
proxy.put('test1', 'test1')
proxy.put('test2', 'test2')
proxy.put('test3', 'test3')
proxy.put('test4', 'test4')

proxy_app = Flask(__name__)

@proxy_app.route('/')
def healthCheck():
    return 'Proxy service up and running...'

@proxy_app.route('/get/<key>')
def get(key):
    val = proxy.get(key)
    return val if val != -1 else f'{key} not found!'

