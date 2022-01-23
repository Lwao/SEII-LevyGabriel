"""
Post author: Chuan Jin
Post link: http://chuanjin.me/2016/08/03/transfer-file/
License: BY-NC-SA 
"""

import socket
import sys

TCP_IP = "127.0.1.1" # socket tcp ip address
FILE_PORT = 5005 # file transfer port
DATA_PORT = 5006 # data transfer port
buf = 1024 # max. buffer length
file_name = sys.argv[1] # get filename from std. input argument

# try: # try invoke connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate TCP socket
sock.connect((TCP_IP, FILE_PORT)) # bind socket to tcp ip and file transfer port
sock.send(file_name.encode('utf-8')) # send file name to receiver
sock.close() # close file socket

print("Sending %s ..." % (file_name)) # print file_name that was sent

f = open(file_name, "rb") # open the file in read mode
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # instantiate TCP socket
sock.connect((TCP_IP, DATA_PORT)) # bind socket to tcp ip and data transfer port
data = f.read() # read file data to 'data'
sock.send(data) # send data in file via data socket to be write by receiver 
sock.close() # close socket connection
f.close() # close file