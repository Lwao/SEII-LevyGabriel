"""
Post author: Chuan Jin
Post link: http://chuanjin.me/2016/08/03/transfer-file/
License: BY-NC-SA 
"""

import socket
import time
import sys

UDP_IP = "127.0.1.1" # socket udp ip address
UDP_PORT = 5005 # input transfer port
buf = 1024 # max. buffer length
file_name = sys.argv[1] # get filename from std. input argument

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # instantiate TCP socket
sock.sendto(file_name.encode('utf-8'), (UDP_IP, UDP_PORT)) # send file_name to ip:port of udp receiver
print ("Sending %s ..." % file_name) # print file name sent

f = open(file_name, "r") # open file in read mode
data = f.read(buf) # read data contained in file
while(data): # while there is data avalaible
    if(sock.sendto(data.encode('utf-8'), (UDP_IP, UDP_PORT))): # send file data to ip:port of udp receiver
        data = f.read(buf) # get more data in file to try sending in the next loop
        time.sleep(0.02) # strutural delay to send and receive data in both ends

# when finish the sending
sock.close() # close udp socket
f.close() # close file