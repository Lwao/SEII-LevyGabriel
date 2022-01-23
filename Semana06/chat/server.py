import socket
import threading
import time

SERVER_IP = socket.gethostbyname(socket.gethostname()) # define server ip based in host 
PORT = 5050 # port to connections
ADDR = (SERVER_IP, PORT) # address tuple with server ip and port
FORMAT = 'utf-8' # format of messages
MSG_MAX_LEN = 1024 # message max. length

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate server socket with socket TCP
server.bind(ADDR) # bound server to address of choice

# memory lists
connections = []
messages = []

def send_messages_ind(connection):
    """
    Send chat stacked messages to a recently connected client via its given connection socket. 
    When a new client sends its name, all stacked messages in the memory of that chat mst be sent to it.

    Parameters
    ----------
    connection : dict
        Dictionary containing variables to establish connection with a given client:
            - "conn" # connection socket
            - "addr" # address bounded to socket
            - "name" # name of client
            - "last" # last message id
    """
    print(f"[SENDING] Seding messages to {connection['addr']}")
    for i in range(connection['last'], len(messages)): # iterate in cronologic order over all messages previous sent 
        seding_message = "msg=" + messages[i] # parse each message to full format
        connection['conn'].send(seding_message.encode()) # send previous parsed message to connection socket of interest
        connection['last'] = i+1 # update last message id (since 'i' starts in 0, the '+1' is mandatory)
        time.sleep(0.2) # structural delay to allow the message to be sent and displayed

def send_messages_all():
    """
    Send new message that arrived in the server to all connections.
    """
    # treat 'connections' list as global variables
    global connections
    for connection in connections: send_messages_ind(connection) # iterate over all connected clients 

def handle_clients(conn, addr):
    """
    Handle clients connections recovering messages.

    Parameters
    ----------
    conn : socket objecvt
        Socket object used to send and receive data during client-server connection.
    addr : tuple
        Address bound to the socket on the client end of the connection.
    """

    print(f"[NEW CONNECTION] A new user has connected by the address {addr}") # message informing that this function is running
    
    # treat 'connections' and 'messages' lists as global variables
    global connections
    global messages
    
    nome = False # client name

    while(True): # loop to get client messages
        msg = conn.recv(MSG_MAX_LEN).decode(FORMAT) # recover message of max. length of 1024-bytes and decode to utf-8
        if(msg): # if message is not null (a message was recovered)
            """ 
            messages must be recovered in the structure below:
                name= ...
                msg= ...
            """
            if(msg.startswith("name=")): # if the actual received message start with 'name=', a.k.a header 
                splited_message = msg.split("=") # split message into list with two itens, the first contains the 'name=' keyword and the second is the payload for the name
                name = splited_message[1] # recover payload of message
                connection_map = { # create connection map with data essential to the current connection
                    "conn": conn, # connection socket
                    "addr": addr, # address bounded to socket
                    "name": name, # name of client
                    "last": 0     # last message id
                }
                connections.append(connection_map) # append connection map to 'connecitons' list
                send_messages_ind(connection_map) # when a new client is identified by its 'name=', all stacked messages in the chat must be update for it
            elif(msg.startswith("msg=")): # if the actual received message start with 'msg=', a.k.a payload
                splited_message = msg.split("=") # split message into list with two itens, the first contains the 'msg=' keyword and the second is the payload
                message = name + "=" + splited_message[1] # relates message payload to client name
                messages.append(message) # append actual message to 'messages' list
                send_messages_all() # when new message arrive in the server, it must be redistributed to all clients



def start():
    """
    Start server socket to listen to new clients and start its connections.
    """

    print("[START] Starting socket") # message informing that this function is running
    server.listen() # socket server is listen to clients
    print(f"[STARTED] Server listen to new messages in address: {ADDR[0]}:{ADDR[1]}") # server is ready to receive messages
    while(True):
        conn, addr = server.accept() # stuck in this line until accept a client connection, saving client connection and address
        thread = threading.Thread(target=handle_clients, args=(conn, addr)) # create thread to handle client connection
        thread.start() # start previous created thread

if __name__ == "__main__":
    start() # starting point of server.py execution