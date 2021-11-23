import os
from routes import proxy_app

if __name__ == '__main__':
    [host, port] = os.getenv('PROXY_ADDRESS').split(':')
    proxy_app.run(host=host, port=port)