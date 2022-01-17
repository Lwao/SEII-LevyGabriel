import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost',15000) # IP + PORT
sock.bind(server_address)

sock.listen(1)

while True:
    print('Waiting new connection!')
    connection, client_address = sock.accept()

    try:
        while True:
            data = connection.recv(100)
            print('received: {!r}'.format(data))

            if data:
                print('Re-sending message to client: ', client_address)
                connection.sendall(data)
            else:
                print('No data received from: ', client_address)
                break
    finally:
        connection.close()
