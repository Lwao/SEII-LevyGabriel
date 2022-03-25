import socket
import threading
import time

PORT = 5050 # port to connect to server
FORMAT = 'utf-8' # format of messages
SERVER = "socket-server-app" # server ip address (ip address may change, so check everytime when running the server)
ADDR = (SERVER, PORT) # address tuple with client ip and port
MSG_MAX_LEN = 1024 # message max. length

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate client socket with socket TCP
client.connect(ADDR)

def reconnect():
    global client
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate client socket with socket TCP
        client.connect(ADDR)
        print('Connected!')
    except: 
        print('Reconnecting...')
        time.sleep(.5)
    

def handle_incoming_msg(conn):
    while True:
        try: 
            server_msg = client.recv(MSG_MAX_LEN).decode(FORMAT) # receive update message from socket server
            if server_msg: # exist server_msg
                conn.send(server_msg) # forward server update msg to mqtt
        except: reconnect()

def handle_forwarding_msg(conn):
    while True:
        if conn.poll(timeout=.1): 
            mqtt_msg = conn.recv() # receive update message from mqtt client
            if mqtt_msg: # exist mqtt_msg
                try: client.send(mqtt_msg.encode(FORMAT)) # forward mqtt update msg to server  
                except: reconnect()

def start_client_socket(conn):
    thread_rcv = threading.Thread(target=handle_incoming_msg, args=(conn,)) # thread to receive messages from server
    thread_send = threading.Thread(target=handle_forwarding_msg, args=(conn,)) # thread to send messages to server

    thread_rcv.start()
    thread_send.start()

if __name__ == "__main__":
    start_client_socket()