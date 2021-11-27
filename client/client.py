import socket
import sys
import os
from dotenv import load_dotenv

load_dotenv()

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket successfully created")
except socket.error as err:
	print("socket creation failed with error %s" %(err))

try:
	host = os.getenv('PROXY_HOST_TCP')
	port = os.getenv('LOCAL_PORT_TCP')
except socket.gaierror:
	print("there was an error resolving the host")
	sys.exit()

# connecting to the server
print(f'Connecting to host: {host} on port: {port}')
s.connect((host, int(port)))

print('the socket has successfully connected')

# Send data
message = b"$4\r\nfoo1\r\n"

print(f'sending: {message}')
s.sendall(message)

data = s.recv(32)
print(f'received: {data}')

print('closing socket')
s.close()