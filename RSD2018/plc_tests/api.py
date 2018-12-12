import sys
import time
import socket

global_score = 0


# PLC communication during the processing of the order
def plc_control(sock, _plc, events):
    
    # Instance to global score
    global global_score

    print ("State: CONNECTED")# in http://" + server_address[0] + ":" + str(server_address[1]) + "/")

    hello = 'hi'
    h = hello.encode()
    sock.send(h)

    print ("Sent hello message")

    # Wait for the PLC to ask for orders
    while True:
        qa = sock.recv(1024)
        q = qa.decode()
        if str(q) == 'new':
            print ("Received PLC request: " + str(q))
            print ("Sending data.")
            break
        
        else:
            print ("Received wrong request from PLC: " + str(q))

        # Prepair data
    d = str(_plc[0]) + ',' + str(_plc[1]) + ',' + str(_plc[2]) 
    data = d.encode()

    # Send data
    sock.send(data)
    print ("Sent order data to PLC.")

    # Listen to updates in the system status. Wait until order is complete and PLC sends PML_Complete
    while True:
        rs = sock.recv(1024)
        if rs != None:
            rec = rs.decode()
            print ("Server's reply: " + str(rec))
            if str(rec) == 'ok':
                print ("The server received the order correctly.")
                print("Waiting for updates...")
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
        else:
            print ("Did not receive anything after sending the order")
    
class manager:

    def __init__(self, cid):
        self.workcell = cid
        print("Starting WorkCell #" + str(cid))
    
    def __del__(self):
        global global_score
        print("Total number of packed boxes: " + str(global_score))
        print("WorkCell #" + str(self.workcell) + " shutdown")