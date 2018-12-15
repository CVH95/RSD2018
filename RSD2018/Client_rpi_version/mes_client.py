#!/usr/bin/python

import mes_api
import socket
import feedback_api
import sys
import time

# Robot System Design 2018 - SDU
# REST API Client of the project's MES System
# Group 3: Carlos, Caroline, Daniel.

argv1 = sys.argv[1]
argv2 = sys.argv[2]
_ip_wlan0 = str(argv2)
_ip_eth0 = str(argv1)

print("\n")
print ("MES client running on wlan0 with IP: " + _ip_wlan0)
print ("PLC client running on eth0 with IP: " + _ip_eth0)

# Define global variables
cell_id = 3
events_dict = {0:'PML_Idle', 1:'PML_Execute', 2:'PML_Complete', 3:'PML_Held', 4:'PML_Suspended', 5:'PML_Aborted', 6:'PML_Stopped', 7:'Order_Start', 8:'Order_Done'}
mes_api._nCycles = 0
mes_api.global_score = 0
mes_api._orderCorrect = 1
mes_api._points_ = 0
mes_api._nStopped = 0
mes_api._nRejected = 0
_chrono_ = 0
mes_api._init_time = mes_api.get_time(23)

file = open("start_time.txt", "w")
file.write("\n \n \n")
file.write("###########\n")
file.write("# SUMMARY #\n")
file.write("###########\n")
file.write("\n")
file.write("\n")
file.write("\n")
file.write("RUNTIME:\n")
file.write("The system was started " + mes_api._init_time + "\n")
file.close()

_wc = mes_api.manager(cell_id)

# Define url and paths

# MES

#_host = 'localhost' # Debug
#_url = 'http://localhost:5000' # Debug
#_plc_addr = _ip_eth0

_host = '192.168.100.200'
_url = 'http://' + _host
_log = '/log'
_orders = '/orders'
_events = '/event_types'

# PLC
_plc_addr = '169.254.112.197'
_plc_port = 6000

# Create a TCP/IP socket client connected to PLC's server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (_plc_addr, _plc_port)
sock.connect(server_address)

#mysql = MySQL()


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
                #mes_api.die(3)

            else:
                print ("Received PLC order request: " + str(q))
                break
                
                #hello = 'hi'
                #h = hello.encode()
                #sock.send(h)
                #print ("Sent hello message again")
            
        print ("Connecting to server on " + _url + " and waiting for an order \n")
    
        ##################################################################
        # 1. SEE ORDERS -- Call GET method to see list of available jobs #
        ##################################################################
    
        resp = mes_api.get_orders(_url, _orders)
        if resp.status_code != 200:
            print ("Raised API Error on GET request. Status code " + str(resp.status_code))
        else:
            print ("GET request " + _url + _orders + " succesful")
            resptime = mes_api.get_time(resp.status_code) 
            print (resptime + "\n")

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
                    _blue_ = jsonObj['orders'][i]['blue']
                    print ("  >> Red: " + str(jsonObj['orders'][i]['red']))
                    _red_ = jsonObj['orders'][i]['red']
                    print ("  >> Yellow: " + str(jsonObj['orders'][i]['yellow']))
                    _yellow_ = jsonObj['orders'][i]['yellow']
                    print ("\n")
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
            mes_api._nCycles = mes_api._nCycles + 1
            #feedback_api.mail_feedback(errSub, errMsg)
            print (errMsg)
            if rerr.status_code != 200:
                print ("Raised API Error on POST request. Status code " + str(rerr.status_code) + "\n")
            else:
                print ("POST request indicating No-Order status to" + _url + " succesful")
                rerrtime = mes_api.get_time(rerr.status_code)
                print (rerrtime + "\n")
                mes_api.die(4)

        else:
            #####################################################
            # 2. TAKE ORDER -- Call PUT method to take an order #
            #####################################################

            r = mes_api.put_order(_url, _orders, _id)
            if r.status_code != 200:
                print ("Raised API Error on PUT request. Status code " + str(r.status_code))
            else:
                succPut = "PUT request " + _url + _orders + " succesful"
                print (succPut)
                rtime = mes_api.get_time(r.status_code)
                print (rtime + "\n")

                # Get the ticket of the order
                jsonPUT = r.json()
                ticket = jsonPUT['ticket']
                putSub = "Order " + str(_id) + " ticket: " + str(ticket)
                print (putSub)

                # Send email notification
                hah = "Order taken and ready to be processed. \n" + "\n"
                putBody = putSub +"\n" + "\n" + hah + rtime
                #feedback_api.mail_feedback(putSub, putBody)
                print (putBody)

                # Call GET method to see 
                r2 = mes_api.get_single(_url, _orders, _id)
                if r2.status_code != 200:
                    print ("Raised API Error on GET. Status code " + str(r2.status_code))
                else:
                    print ("GET request " + _url + _orders + " succesful")
                    r2time = mes_api.get_time(r2.status_code)
                    print (r2time + "\n")

                    # Call POST method to add new log entry on Order_Start
                    _idstr = str(_id)
                    cmnt = _idstr + ", " + str(ticket)
                    r3 = mes_api.post_log(_url, _log, cell_id, cmnt, events_dict[7])
                    if r3.status_code != 200:
                        print ("Raised API Error on POST request. Status code " + str(r3.status_code))
                    else:
                        print ("POST request " + _url + _log + " succesful")
                        r3time = mes_api.get_time(r3.status_code)
                        print (r3time + "\n")

                #####     Order processing      #####
                    
                print ("Processing order... \n")
                #mes_api.die(15)
                #mes_api.global_score = mes_api.global_score + 1
                print (" #### CONNECTING TO PLC SERVER #### \n \n \n")
                print ("Connecting to PLC Server in http://" + _plc_addr + ":" + str(_plc_port) + "/")
                cmnt = str(_id) + ", " + str(ticket)
                _chrono_ = 0
                init = time.time()
                mes_api.plc_control(sock, _plc, events_dict, _url, _log, cell_id, cmnt)
                finit = time.time()
                _chrono_ = finit - init
                
                # Check if the order parameters were correct
                _how = mes_api._orderCorrect
                if _how > 0 and _how < 9:
                    print ("Order was completed succesfully: " + str(_how) + ". Total time: " + str(_chrono_) + " seconds.")
                    _acc_ = mes_api.count_points(_red_, _blue_, _yellow_, 1, _chrono_, _id)
                    mes_api._points_ = mes_api._points_ + _acc_
                    print ("Total orders completed: " + str(mes_api.global_score) + " boxes.")
                    print ("Total score: " + str(mes_api._points_) + " points.")
                    tii = mes_api.get_time(911)
                    print (tii + "\n \n \n")

                    ##### Order processing code above  #####

            
                    ##########################################################################
                    # 3. DELETE ORDER -- Call DELETE method to erase completed order from DB #
                    ##########################################################################
                    resp = mes_api.delete_order(_url, _orders, _id, ticket)
                    if resp.status_code != 200:
                        print ("Raised API Error on DELETE request. Status code " + str(resp.status_code))
                    else:
                        succDel = "DELETE request " + _url + _orders + " succesful"
                        print (succDel)
                        deltime = mes_api.get_time(resp.status_code) 
                        print (deltime + "\n")

                        # Send email notification
                        lal = "Order " + str(_id) + " completed. \n \n Total score: " + str(mes_api._points_) + " points. \n" + "\n"
                        delBody = succDel + "\n" + "\n" + lal + deltime
                        print (delBody)
                        #feedback_api.mail_feedback(putSub, delBody)                

                        # POST Log entry indicating deletion of the complete order
                        r4 = mes_api.post_log(_url, _log, cell_id, cmnt, events_dict[8])
                        if r4.status_code != 200:
                            print ("Raised API Error on POST request. Status code " + str(r4.status_code))
                        else:
                            print ("POST request " + _url + _log + " succesful")
                            r4time = mes_api.get_time(r4.status_code)
                            print (r4time + "\n")
                            mes_api._nCycles = mes_api._nCycles + 1
                            print ("The system has been running for " + str(mes_api._nCycles) + " cycles. Score: " + str(mes_api._points_))
                            print ("\n \n \n")
                
                elif _how > 10: 
                    print ("\n" + "The order was CANCELLED: " + str(_how))
                    print ("Something went wrong while processing, the system went STOPPED")
                    mes_api._nStopped = mes_api._nStopped + 1
                    mes_api._nCycles = mes_api._nCycles + 1
                    r11 = mes_api.delete_order(_url, _orders, _id, ticket)
                    if r11.status_code != 200:
                        print ("Raised API Error on DELETE request. Status code " + str(r11.status_code))
                    else:
                        succDel = "DELETE request " + _url + _orders + " succesful"
                        print (succDel)
                        deltime = mes_api.get_time(r11.status_code) 
                        print (deltime + "\n")
                        # POST Log entry indicating deletion of the complete order
                        cmnt = "Order " + str(_id) + " was STOPPED"
                        r17 = mes_api.post_log(_url, _log, cell_id, cmnt, events_dict[6])
                        if r17.status_code != 200:
                            print ("Raised API Error on POST request. Status code " + str(r17.status_code))
                        else:
                            print ("POST request " + _url + _log + " succesful")
                            r17time = mes_api.get_time(r17.status_code)
                            print (r17time + "\n")
                            print ("The system has been running for " + str(mes_api._nCycles) + " cycles. Score: " + str(mes_api._points_))
                            print ("\n \n \n")
                    print ("Starting a new cycle \n \n")
                    
                
                else:
                    print ("\n The order was REJECTED: " + str(_how))
                    mes_api._nRejected = mes_api._nRejected + 1
                    mes_api._nCycles = mes_api._nCycles + 1
                    r11 = mes_api.delete_order(_url, _orders, _id, ticket)
                    if r11.status_code != 200:
                        print ("Raised API Error on DELETE request. Status code " + str(r11.status_code))
                    else:
                        succDel = "DELETE request " + _url + _orders + " succesful"
                        print (succDel)
                        deltime = mes_api.get_time(r11.status_code) 
                        print (deltime + "\n")
                        # POST Log entry indicating deletion of the complete order
                        cmnt = "Order " + str(_id) + " was REJECTED"
                        r18 = mes_api.post_log(_url, _log, cell_id, cmnt, events_dict[0])
                        if r18.status_code != 200:
                            print ("Raised API Error on POST request. Status code " + str(r18.status_code))
                        else:
                            print ("POST request " + _url + _log + " succesful")
                            r18time = mes_api.get_time(r18.status_code)
                            print (r18time + "\n")
                            print ("The system has been running for " + str(mes_api._nCycles) + " cycles. Score: " + str(mes_api._points_))
                            print ("\n \n \n")
                    print ("Starting a new cycle \n \n")
                    
except KeyboardInterrupt:
    print ("\n \n \n \n \n \n \n \n \n \n \n")
    print ("Operation interrupted.")
    print ("Closing connection to MES server: " + _host)
    print ("Closing connection to MES server: " + _plc_addr + ":" + str(_plc_port))
    print ("Shutting down... \n \n \n \n \n")

# Never ending loop
