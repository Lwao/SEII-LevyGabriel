import socket
import time

PORT = 5050 # port to connect to server
FORMAT = 'utf-8' # format of messages
#SERVER = "socket-server-app" # server ip address (ip address may change, so check everytime when running the server)
SERVER = "NocturnalPeriwinkle" # server ip address (ip address may change, so check everytime when running the server)
ADDR = (SERVER, PORT) # address tuple with client ip and port
MSG_MAX_LEN = 1024 # message max. length

def start_client_socket():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate client socket with socket TCP

    while True:
        try:
            # msg = client.recv(MSG_MAX_LEN).decode(FORMAT) # receive introduction msg of server
            # if msg: print(msg)
            client.send('Hello server!'.encode(FORMAT)) # send introduction msg to server
            time.sleep(0.1)
        except: # try to reconnect
            try: 
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate client socket with socket TCP
                client.connect(ADDR)
            except socket.error as error: time.sleep(0.1)

if __name__ == "__main__":
    start_client_socket()