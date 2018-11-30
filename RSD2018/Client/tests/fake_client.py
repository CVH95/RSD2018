#!/usr/bin/python

import socket
import sys


server_add = ('169.254.112.197', 5000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_add)

print ("Connected to server in PLC")

data = '1'

sock.send(data)

print ("Sent data")

while True:
    rec = sock.recv(1024)
    if rec !=  None:
        print ("received: " + rec)
        break

sock.close()
print ("Connection closed")

        


