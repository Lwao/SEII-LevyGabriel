"""
Post author: Chuan Jin
Post link: http://chuanjin.me/2016/08/03/transfer-file/
License: BY-NC-SA 
"""

import socket
import select

UDP_IP = "127.0.1.1" # socket udp ip address
IN_PORT = 5005 # input transfer port
timeout = 3 # timeout in seconds
buf = 1024 # max. buffer length

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # instantiate UDP socket
sock.bind((UDP_IP, IN_PORT)) # bind socket to udp ip and file transfer port

while True:
    data, addr = sock.recvfrom(buf) # recover data continuously from sender and ip address
    if data:
        print("File name:" % data) # received file name
        file_name = 'new_' + data.strip().decode() # remove useless spaces to compose file name and create new file

    f = open(file_name, 'wb') # open file based in the received file name write mode

    while True:
        ready = select.select([sock], [], [], timeout) # select udp datagram in given socket and wait for 'timeout' seconds for each datagram to finish connection
        print(ready)
        if ready[0]: # if data
            data, addr = sock.recvfrom(1024) # recover data and origin address
            f.write(data) # write recover data from file into new file downloaded
        else:
            print("%s finish!" % file_name) # if there is no datagram ready
            f.close() # close file and...
            break # break loop