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

    # 1. Receive list of lego bricks = array[4]
        # index =
            # 0: blue
            # 1: red
            # 2: yellow
            # 3: order id
    message = c.recv(1024)
        
    if message == 'hi':
        print "Received hello message: " + message
        ans = 'new'
        c.send(ans)
        print "Sent: " + ans
        
    else:

        # 2. Robot starts working. PackML sends state updates to MES system via socket.

        print "Order: " + message
        b = 'ok'
        c.send(b)
        i = 0
        j = random.randint(2,6)
        print "Number of rounds = " + str(j)
        while (i<j):
            a = random.randint(0,5)
            if a == 2:
                a = 0
            else:
                a = a
            _a = str(a)
            c.send(_a)
            print "Sending PackML state upadate."
            time.sleep(3)
            i = i + 1
        eoc = 2
        i = 0
        _eoc = str(eoc)
        c.send(_eoc)
        #break

#print "Server shut down"