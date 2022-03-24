# python -m pipreqs.pipreqs

import multiprocessing
import sys
import time

from mqtt_client import *
from socket_client import *

if __name__ == "__main__":
    mqttConn, socketConn = multiprocessing.Pipe()

    mqtt_process = multiprocessing.Process(target=start_mqtt_client, args=(mqttConn,)) # thread to handle mqtt client
    socket_process = multiprocessing.Process(target=start_client_socket, args=(socketConn,)) # thread to communicate with webserver
    
    mqtt_process.start()
    time.sleep(.2)
    socket_process.start()
    time.sleep(.2)

    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        print('Exiting...')
        mqtt_process.terminate()
        socket_process.terminate()
        print('Processes successfully closed')
        sys.exit()