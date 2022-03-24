# python -m pipreqs.pipreqs

import multiprocessing
import sys
import time

from socket_server import *

def flask_app(conn):
    while True:
        conn.send('Message from Flask')
        time.sleep(1)
        if conn.poll(timeout=.1): 
            msg = conn.recv()
            if msg: print('Flask app -> ' + msg)


if __name__ == "__main__":
    flaskConn, socketConn = multiprocessing.Pipe()

    server_process = multiprocessing.Process(target=start_server_socket, args=(socketConn,)) 
    flask_process = multiprocessing.Process(target=flask_app, args=(flaskConn,)) 

    server_process.start()
    flask_process.start()

    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        print('Exiting...')
        server_process.terminate()
        flask_process.terminate()
        print('Processes successfully closed')
        sys.exit()