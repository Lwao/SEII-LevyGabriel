"""
Post author: Chuan Jin
Post link: http://chuanjin.me/2016/08/03/transfer-file/
License: BY-NC-SA 
"""

import socket

TCP_IP = "127.0.1.1" # socket tcp ip address
FILE_PORT = 5005 # file transfer port
DATA_PORT = 5006 # data transfer port
timeout = 3 # timeout in seconds
buf = 1024 # max. buffer length

sock_f = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate TCP socket
sock_f.bind((TCP_IP, FILE_PORT)) # bind socket to tcp ip and file transfer port
sock_f.listen(1) # put socket in listen state for new messages

sock_d = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate TCP socket
sock_d.bind((TCP_IP, DATA_PORT)) # bind socket to tcp ip and data transfer port
sock_d.listen(1) # put socket in listen state for new messages

while True:
    conn, addr = sock_f.accept() # accept connection from file sender and get connection socket and address
    data = conn.recv(buf).decode() # recover file name from sender with max. buffer length
    if data: # if there is data
        print("File name: %s" % (data)) # print received file name
        file_name = 'new_' + data.strip() # remove useless spaces to compose file name and create new file

    f = open(file_name, 'wb') # open file based in the received file name write mode

    conn, addr = sock_d.accept() # accept connection from data sender and get connection socket and address
    while True: # after get the file, recover data and write to it
        data = conn.recv(buf).decode() # recover data received in tcp socket
        if not data: # if there is no data received, break the loop
            break
        f.write(data.encode('utf-8')) # while data is received, keep writing to file

    print ("%s finish!" % (file_name)) # when no data is received, print finish message and...
    f.close() # ... close the file