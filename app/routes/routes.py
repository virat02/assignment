from flask import Flask
from package.proxy.proxy_service import Proxy

# Initialize Proxy
proxy = Proxy(is_tcp=False)

proxy_app = Flask(__name__)

@proxy_app.route('/')
def healthCheck():
    return 'Proxy service up and running...'

@proxy_app.route('/get/<key>')
def get(key):
    val = proxy.get(key)
    return val if val != -1 else f'{key} not found!'

