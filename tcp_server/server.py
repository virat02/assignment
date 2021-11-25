import os, socket		
from package.proxy.proxy_service import Proxy

# create a socket object
s = socket.socket()		
print('Socket successfully created')

host = os.getenv('PROXY_HOST')
port = os.getenv('PROXY_PORT')		

# bind to the host and port from .env
s.bind((host, int(port)))		
print(f'socket bounded to host: {host} on port: {port}')

# put the socket into listening mode
s.listen(5)	
print('socket is listening')		

# initialize Proxy
proxy = Proxy(is_tcp=True)


while True:
    # Establish connection with client.
    c, addr = s.accept()	
    print(f'Got connection from {addr}')

    request = c.recv(32)
    key = request.decode("utf-8")

    print(f'Requesting proxy to get {key}')
    response = proxy.get(key)

    print(f'Received from proxy {response}')
    c.send(response.encode("utf-8"))

    c.close()
