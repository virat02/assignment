import os
from routes.routes import proxy_app

if __name__ == '__main__':
    host = os.getenv('PROXY_HOST')
    port = os.getenv('PROXY_PORT')
    proxy_app.run(host=host, port=port)