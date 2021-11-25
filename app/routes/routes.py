from flask import Flask
from package.proxy.proxy_service import Proxy

# initialize Proxy
proxy = Proxy()

proxy_app = Flask(__name__)

@proxy_app.route('/')
def healthCheck() -> str:
    """Returns whether proxy service is up"""
    return 'Proxy service up and running...'

@proxy_app.route('/get/<key>')
def get(key: str) -> str:
    """Maps the http get requests to proxy get request"""
    return proxy.get(key)
    

