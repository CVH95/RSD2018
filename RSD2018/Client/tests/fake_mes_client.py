#!/usr/bin/python

import socket
import sys

events_dict = {0:'PML_Idle', 1:'PML_Execute', 2:'PML_Complete', 3:'PML_Held', 4:'PML_Suspended', 5:'PML_Aborted', 6:'PML_Stopped', 7:'Order_Start', 8:'Order_Done'}

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 30000)
sock.connect(server_address)

print "Connected to PLC's Server in http://" + server_address[0] + ":" + str(server_address[1]) + "/"

_plc = [1,2,1,49]
data = str(_plc)

sock.send(data)

print "Sent order " + data

while True:
    rcpt = sock.recv(1024)
    _state = int(rcpt)
    if _state == 9:
        break
    else:
        print "Server's reply:"
        print "PackML state = " + events_dict[_state]


sock.close()
print "Connection closed."