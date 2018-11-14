#!/usr/bin/python

import socket
import sys
import random
import time

_ip = 'localhost'
_port = 30000

print "PLC running TCP/IP Server on http://" + _ip + ":" + str(_port) + "/"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((_ip, _port))
server.listen(5)  # max backlog of connections
(c, addr) = server.accept() 



while (True): 
    print "Accepted connection from {}:{}".format(addr[0], addr[1])
    _order = c.recv(1024)
    if _order != '':
        # Check if received and reply back:
        print "Order: " + _order
        i = 0
        j = random.randint(2,6)
        while (i<j):
            a = random.randint(0,6)
            _a = str(a)
            c.send(_a)
            print "Sending PackML state upadate."
            i = i + 1
            time.sleep(3)
        eoc = 9
        i = 0
        _eoc = str(eoc)
        c.send(_eoc)
        break

print "Server shut down"