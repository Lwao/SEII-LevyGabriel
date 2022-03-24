import socket
import select

SERVER_IP = socket.gethostbyname(socket.gethostname()) # define server ip based in host 
PORT = 50500 # port to connections
ADDR = (SERVER_IP, PORT) # address tuple with server ip and port
FORMAT = 'utf-8' # format of messages
MSG_MAX_LEN = 1024 # message max. length
TIMEOUT_S = 1

def start_server_socket(conn):
    print(f"Socket host name: %s" % socket.gethostname())

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate server socket with socket TCP
    server.bind(ADDR) # bound server to address of choice

    while True: 
        print('Listen...')
        server.listen() # socket server is listen to clients
        conn_client, addr = server.accept() # stuck in this line until accept a client connection, saving client connection and address    
        print('Connected!')
        while True: # receive messages until connection error
            if conn.poll(timeout=.1): 
                flask_msg = conn.recv() # receive update message from flask client
                if flask_msg: # exist flask_msg
                    conn_client.send(flask_msg.encode(FORMAT)) # forward flask update msg to client    
            
            print('rec1')
            client_msg = conn_client.recv(MSG_MAX_LEN).decode(FORMAT) # receive update message from socket client
            print('rec2')
            if(client_msg): # exist client message
                conn.send(client_msg) # forward server update msg to flask
            
              
if __name__ == "__main__":
    start_server_socket()