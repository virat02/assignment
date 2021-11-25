# first of all import the socket library
import os, socket		
from package.proxy.proxy_service import Proxy

# next create a socket object
s = socket.socket()		
print('Socket successfully created')

# reserve a port on your computer in our
# case it is 12345 but it can be anything
host = os.getenv('PROXY_HOST')
port = os.getenv('PROXY_PORT')		

# bind to the port
s.bind((host, int(port)))		
print(f'socket bounded to host: {host} on port: {port}')

# put the socket into listening mode
s.listen(5)	
print('socket is listening')		

# Initialize Proxy
proxy = Proxy(is_tcp=True)

# Establish connection with client.
while True:
    c, addr = s.accept()	
    print(f'Got connection from {addr}')

    request = c.recv(32)
    key = request.decode("utf-8")

    print(f'Requesting proxy to get {key}')
    response = proxy.get(key)

    print(f'Received from proxy {response}')

    response = response if response != -1 else f'{key} not found!'

    c.send(response.encode("utf-8"))

    c.close()
