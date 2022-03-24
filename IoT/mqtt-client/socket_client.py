import socket
import time

PORT = 50500 # port to connect to server
FORMAT = 'utf-8' # format of messages
SERVER = "socket-server-app" # server ip address (ip address may change, so check everytime when running the server)
ADDR = (SERVER, PORT) # address tuple with client ip and port
MSG_MAX_LEN = 1024 # message max. length

def start_client_socket(conn):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate client socket with socket TCP

    while True:
        try:
            if conn.poll(timeout=.1): 
                mqtt_msg = conn.recv() # receive update message from mqtt client
                if mqtt_msg: # exist mqtt_msg
                    client.send(mqtt_msg.encode(FORMAT)) # forward mqtt update msg to server    
            print('here')
            server_msg = client.recv(MSG_MAX_LEN).decode(FORMAT) # receive update message from socket server
            if server_msg: # exist server_msg
                conn.send(server_msg) # forward server update msg to mqtt
            print('pass')
            time.sleep(.1)
        except: # try to reconnect to server
            try: 
                print('Trying connection...')
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate client socket with socket TCP
                client.connect(ADDR)
                print('Connected!')
            except socket.error as error: time.sleep(.1)

if __name__ == "__main__":
    start_client_socket()