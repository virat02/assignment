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
print (f'socket bounded to host: {host} on port: {port}')

# put the socket into listening mode
s.listen(5)	
print ('socket is listening')		

# Initialize Proxy
proxy = Proxy(is_tcp=True)

# set test data for the time being.
proxy.put("$3\r\nfoo\r\n", "$3\r\nbar\r\n")
proxy.put("$4\r\nfoo1\r\n", "$4\r\nbar1\r\n")
proxy.put("$4\r\nfoo2\r\n", "$4\r\nbar2\r\n")
proxy.put("$4\r\nfoo3\r\n", "$4\r\nbar3\r\n")
proxy.put("$4\r\nfoo4\r\n", "$4\r\nbar4\r\n")
proxy.put("$4\r\nfoo5\r\n", "$4\r\nbar5\r\n")

# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client.
    c, addr = s.accept()	
    print(f'Got connection from {addr}')
    
    try:
        request = c.recv(32)
        
        key = request.decode("utf-8")
        response = proxy.get(key)
        response = response if response != -1 else f'{key} not found!'
        c.send(response.encode("utf-8"))

    finally:
        c.close()
        break
