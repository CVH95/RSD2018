#!/usr/bin/python

import mes_api
import socket


# Define url and paths
#_host = 'localhost' # Debug
#_url = 'http://' + _host + ':5000'

# MES
_host = '192.168.100.200'
_url = 'http://' + _host
_log = '/log'
_orders = '/orders'
_events = '/event_types'

# PLC
_ip = '192.168.100.107'
_port = 6000

# Define global variables
cell_id = 3
events_dict = {0:'PML_Idle', 1:'PML_Execute', 2:'PML_Complete', 3:'PML_Held', 4:'PML_Suspended', 5:'PML_Aborted', 6:'PML_Stopped', 7:'Order_Start', 8:'Order_Done'}
mes_api.global_score = 0


# Create a TCP/IP socket client connected to PLC's server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (_ip, _port)
sock.connect(server_address)

try:
    while True:
        
        print ("Status: CONNECTED on eth0.")

        hello = 'hi'
        h = hello.encode()
        sock.send(h)

        print ("Sent hello message")

        # Wait for the PLC to ask for orders
        while True:
            qa = sock.recv(1024)
            q = qa.decode()
            if str(q) != 'new':
                print ("Received update on WorkCell status from PLC: " + str(q))
                mes_api.die(1)
                #hello = 'hi'
                #h = hello.encode()
                #sock.send(h)
                #print ("Sent hello message again")
                

            else:
                print ("Received PLC order request: " + str(q))
                break


        print (" #### CONNECTED TO MES SERVER #### \n \n \n")
        print ("Connecting to server on " + _url + " and waiting for new jobs \n")
        resp = mes_api.get_orders(_url, _orders)
        if resp.status_code != 200:
            print ("Raised API Error on GET request. Status code " + str(resp.status_code))
        else:
            print ("GET request " + _url + _orders + " succesful")
            resptime = mes_api.get_time(resp.status_code) 
            print (resptime)

            # Create JSON object
            jsonObj = resp.json()
    
            # Check & Print JSON object array length
            lgth = len(jsonObj['orders'])
            #print "  >> JSON object length = " + str(lgth) + "\n"

            # Seek for orders with status == ready
            for i in range(0, lgth):
                if jsonObj['orders'][i]['status'] == 'ready':
                    _id = jsonObj['orders'][i]['id']
                    # Array that will be sent to the PLC
                    _plc = [jsonObj['orders'][i]['blue'], jsonObj['orders'][i]['red'], jsonObj['orders'][i]['yellow'], _id]
                    print ("Taking order #" + str(_id))
                    print ("Updated order with id: " + str(_id))
                    print ("Preparing LEGO bricks:")
                    print ("  >> Blue: " + str(jsonObj['orders'][i]['blue']))
                    print ("  >> Red: " + str(jsonObj['orders'][i]['red']))
                    print ("  >> Yellow: " + str(jsonObj['orders'][i]['yellow']))
                    print ("\n \n \n")
                    break
                else:
                    _id = -1

        
        # Handling situation in which no order is avaliable.
        if _id == -1:
            cerr = "waiting - all orders taken"
            rerr = mes_api.post_log(_url, _log, cell_id, cerr, events_dict[0])
            Msg = "No order is available at the moment. System is waiting. \n \n"
            errSub = "WARNING! All orders taken!"
            rerrtime = mes_api.get_time(rerr.status_code)
            errMsg = Msg + rerrtime
            print (errMsg)
            #feedback_api.mail_feedback(errSub, errMsg)
            if rerr.status_code != 200:
                print ("Raised API Error on POST request. Status code " + str(rerr.status_code) + "\n")
            else:
                print ("POST request indicating No-Order status to " + _url + " succesful")
                rerrtime = mes_api.get_time(rerr.status_code)
                print (rerrtime + "\n \n")
                mes_api.die(8)

        # Connect to PLC and send order
        else:
            cmt = "is a test"
            print (" #### CONNECTED TO PLC SERVER #### \n \n \n")
            print ("Connecting to PLC Server in http://" + _ip + ":" + str(_port) + "/")
            mes_api.plc_control(sock, _plc, events_dict, _url, _log, cell_id, cmt)
            print ("Order was completed succesfully. ")
            print ("Total orders completed: " + str(mes_api.global_score))
            print ("Rebboting the cycle...")
            tii = mes_api.get_time(911)
            print (tii + "\n \n \n")

except KeyboardInterrupt:
    print("\n" + "Operation Interrupted. Exiting... \n")