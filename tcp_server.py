# first of all import the socket library
import os, socket			

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

# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client.
    c, addr = s.accept()	
    print(f'Got connection from ${addr}, conn: ${c}')

    # send a thank you message to the client. encoding to send byte type.
    c.send('Thank you for connecting'.encode())
    
    data = c.recv(16)
    print(f'received data: ${data}')
    c.send(f'Got your message: ${data}'.encode())
    # finally:
    #     c.close()
    #     break
