import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost',15000) # IP + PORT
print('Connecting to - {}:{}'.format(*server_address))

try:
    sock.connect(server_address)
    msg = b'Message send by the client'
    tam = len(msg)
    for i in range(5):
        inp = input("Press RETURN to continue...")
        print(i+1, msg)
        sock.sendall(msg)
finally: pass