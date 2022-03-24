# python -m pipreqs.pipreqs

import multiprocessing
import sys
import time

from socket_server import *

if __name__ == "__main__":
    server_process = multiprocessing.Process(target=start_server_socket) 
    server_process.start()

    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        print('Exiting...')
        server_process.terminate()
        print('Processes successfully closed')
        sys.exit()