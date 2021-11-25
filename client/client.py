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
	host = "localhost"
	port = 8081
except socket.gaierror:
	print("there was an error resolving the host")
	sys.exit()

print(f'Connecting to host: {host} on port: {port}')
# connecting to the server
s.connect((host, int(port)))

print('the socket has successfully connected')

try:
	# Send data
	message = b"$4\r\nfoo6\r\n"
	print(f'sending: {message}')
	s.sendall(message)
	
	data = s.recv(32)
	print(f'received: {data}')
	
finally:
	print('closing socket')
	s.close()