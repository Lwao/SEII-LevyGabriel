import socket
import threading
import time

PORT = 5050 # port to connect to server
FORMATO = 'utf-8' # format of messages
SERVER = "127.0.1.1" # server ip address (ip address may change, so check everytime when running the server)
ADDR = (SERVER, PORT) # address tuple with client ip and port
MSG_MAX_LEN = 1024 # message max. length

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate client socket with socket TCP
client.connect(ADDR) # connect client to server in given address

def handle_messages():
    """
    Handle recovered messages from server printing on client screen.
    """
    while(True):
        msg = client.recv(MSG_MAX_LEN).decode() # decode recovered messages from server
        splited_message = msg.split("=") # split 'msg=' header from message payload
        print(splited_message[1] + ": " + splited_message[2]) # print message to std. output in the format "author name: payload"

def send(message):
    """
    Send custom message encoded to server.

    Parameters
    ----------
    message : string
        String containing message to send to server.
    """
    client.send(message.encode(FORMATO)) # send message to server

def send_message():
    """
    Send client message to server.
    """
    message = input() # wait for std. input to store client custom message
    send("msg=" + message) # send client message to server

def send_name():
    """
    Send client name to server.
    """
    name = input('Type your name: ') # wait for std. input to store client name
    send("name=" + name) # send client name to server

def start_sending():
    """
    Send client message in the format:
        name= ...
        msg= ...
    """
    send_name()
    send_message()

def start_client():
    """
    Start client on threads instantiation to work handling incoming messages and sending messages in parallel.
    """
    thread1 = threading.Thread(target=handle_messages) # thread to receive messages from server
    thread2 = threading.Thread(target=start_sending) # thread to send client messages

    # start created threads
    thread1.start()
    thread2.start()

if __name__ == "__main__":
    start_client() # starting point of client.py execution