import socket
import select

def handle_incoming_msg(msg):
    print(msg)

def start_server_socket():
    print(f"Socket host name: %s" % socket.gethostname())
    SERVER_IP = socket.gethostbyname(socket.gethostname()) # define server ip based in host 
    PORT = 50500 # port to connections
    ADDR = (SERVER_IP, PORT) # address tuple with server ip and port
    FORMAT = 'utf-8' # format of messages
    MSG_MAX_LEN = 1024 # message max. length
    TIMEOUT_S = 1

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate server socket with socket TCP
    server.bind(ADDR) # bound server to address of choice
    

    while True: 
        print('Listen...')
        server.listen() # socket server is listen to clients
        conn, addr = server.accept() # stuck in this line until accept a client connection, saving client connection and address    
        print('Connected!')
        while True: # receive messages until connection error
            msg = conn.recv(MSG_MAX_LEN).decode(FORMAT) # receive introduction msg of client
            if(msg): # if message is not null (a message was recovered)
                handle_incoming_msg(msg)
            else: break
              
            

if __name__ == "__main__":
    start_server_socket()