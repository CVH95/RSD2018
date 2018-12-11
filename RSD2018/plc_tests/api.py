import sys
import time
import socket

global_score = 0

# PLC communication during the processing of the order
def plc_control(sock, _plc, events):
    
    # Instance to global score
    global global_score

    print ("Connected to PLC's Server")# in http://" + server_address[0] + ":" + str(server_address[1]) + "/")

    hello = 'hi'
    h = hello.encode()
    sock.send(h)

    print ("Sent hello message")

    # Wait for the PLC to ask for orders
    while True:
        qa = sock.recv(1024)
        q = qa.decode()
        if q == 'new':
            print ("Received PLC request: " + str(q))
            print ("Sending data.")
            break
        else:
            print ("Received wronf request from PLC.")

    # Prepair data
    d = str(_plc[0]) + ',' + str(_plc[1]) + ',' + str(_plc[2]) 
    data = d.encode()

    # Send data
    sock.send(data)
    print ("Sent order data to PLC.")

    # Listen to updates in the system status. Wait until order is complete and PLC sends PML_Complete
    while True:
        rs = sock.recv(1024)
        rec = rs.decode()
        if str(rec) == 'ok':
            print ("Server's reply: " + str(rec))
            print ("The server received the order correctly")
            while True:
                rcpt = sock.recv(1024)
                _state = rcpt.decode()
                if int(_state) == 2:
                    print ("Server's reply: " + _state)
                    print ("PackML state update: " + events[int(_state)])
                    global_score = global_score + 1
                    break
                else:
                    print ("Server's reply: " + _state)
                    print ("PackML state update: " + events[int(_state)])
                    #evt = events[_state]
                    #post_log(_url, _path, cid, cmt, evt)
                    
            break
            
        else:
            print ("Server's reply: " + str(rec))
            print ("An error ocurred while sending the order. Re-sending...")
            plc_control(sock, _plc, events)
                
    #sock.close()
    #print ("Connection closed.")