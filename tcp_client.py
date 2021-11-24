import socket
import sys
import os

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket successfully created")
except socket.error as err:
	print("socket creation failed with error %s" %(err))

# default port for socket to listen to
port = 6379

try:
	# TODO: Make it listen to proxy service rather than redis
	[host, port] = os.getenv('BACKING_REDIS_ADDRESS').split(':')
except socket.gaierror:
	print("there was an error resolving the host")
	sys.exit()

# connecting to the server
s.connect((host, int(port)))

print('the socket has successfully connected')

try:
    # Send data
    # message = b'*2\r\n$3\r\nSET\r\n$5\r\ncolor\r\n$3\r\nred\r\n'
	message = b'*1\r\n$4\r\nPING\r\n'
	print(f'sending: {message}')
	s.sendall(message)
	
	data = s.recv(16)
	print(f'received: {data}')
        
finally:
    print('closing socket')
    s.close()