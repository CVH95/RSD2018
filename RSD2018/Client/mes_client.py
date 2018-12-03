#!/usr/bin/python

import mes_api
import feedback_api

# Robot System Design 2018 - SDU
# REST API Client of the project's MES System
# Group 3: Carlos, Caroline, Daniel.

print "##################################"
print "##  WORKCELL #3 ONLINE MANAGER  ##"
print "################################## \n"

# Define url and paths
#_host = 'localhost' # Debug
_host = '192.168.100.200'
#_url = 'http://' + _host + ':5000'
_url = 'http://' + _host
_log = '/log'
_orders = '/orders'
_events = '/event_types'

# Define global variables
cell_id = 3
events_dict = {0:'PML_Idle', 1:'PML_Execute', 2:'PML_Complete', 3:'PML_Held', 4:'PML_Suspended', 5:'PML_Aborted', 6:'PML_Stopped', 7:'Order_Start', 8:'Order_Done'}
mes_api.global_score = 0

#mysql = MySQL()

while True:

    print "Connecting to server on " + _url + " and waiting for new jobs \n"
    
    ##################################################################
    # 1. SEE ORDERS -- Call GET method to see list of available jobs #
    ##################################################################
    
    resp = mes_api.get_orders(_url, _orders)
    if resp.status_code != 200:
        print "Raised API Error on GET request. Status code " + str(resp.status_code)
    else:
        print "GET request " + _url + _orders + " succesful"
        resptime = mes_api.get_time(resp.status_code) 
        print resptime

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
                print "Taking order #" + str(_id)
                print "Updated order with id: " + str(_id)
                print "Preparing LEGO bricks:"
                print "  >> Blue: " + str(jsonObj['orders'][i]['blue'])
                print "  >> Red: " + str(jsonObj['orders'][i]['red'])
                print "  >> Yellow: " + str(jsonObj['orders'][i]['yellow'])
                print "\n"
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
        print errMsg
        #feedback_api.mail_feedback(errSub, errMsg)
        if rerr.status_code != 200:
            print "Raised API Error on POST request. Status code " + str(rerr.status_code) + "\n"
        else:
            print "POST request indicating No-Order status to " + _url + " succesful"
            rerrtime = mes_api.get_time(rerr.status_code)
            print rerrtime
            mes_api.die(8)

    else:
        #####################################################
        # 2. TAKE ORDER -- Call PUT method to take an order #
        #####################################################

        r = mes_api.put_order(_url, _orders, _id)
        if r.status_code != 200:
            print "Raised API Error on PUT request. Status code " + str(r.status_code)
        else:
            succPut = "PUT request " + _url + _orders + " succesful"
            print succPut
            rtime = mes_api.get_time(r.status_code)
            print rtime

            # Get the ticket of the order
            jsonPUT = r.json()
            ticket = jsonPUT['ticket']
            putSub = "Order " + str(_id) + " ticket: " + str(ticket)
            print putSub

            # Send email notification
            hah = "Order taken and ready to be processed. \n" + "\n"
            putBody = putSub +"\n" + "\n" + hah + rtime
            print putBody
            #feedback_api.mail_feedback(putSub, putBody)

            # Call GET method to see 
            r2 = mes_api.get_single(_url, _orders, _id)
            if r2.status_code != 200:
                print "Raised API Error on GET. Status code " + str(r2.status_code)
            else:
                print "GET request " + _url + _orders + " succesful"
                r2time = mes_api.get_time(r2.status_code)
                print r2time

                # Call POST method to add new log entry on Order_Start
                _idstr = str(_id)
                cmnt = _idstr + ", " + str(ticket)
                r3 = mes_api.post_log(_url, _log, cell_id, cmnt, events_dict[7])
                if r3.status_code != 200:
                    print "Raised API Error on POST request. Status code " + str(r3.status_code)
                else:
                    print "POST request " + _url + _log + " succesful"
                    r3time = mes_api.get_time(r3.status_code)
                    print r3time

            #####     Order processing      #####
            print "Processing order... \n"
            mes_api.die(25)
            #mes_api.plc_control(_plc, events_dict, _url, _log, cell_id, cmnt)


            ##### PackML related code here  #####

            
            ##########################################################################
            # 3. DELETE ORDER -- Call DELETE method to erase completed order from DB #
            ##########################################################################
            resp = mes_api.delete_order(_url, _orders, _id, ticket)
            if resp.status_code != 200:
                print "Raised API Error on DELETE request. Status code " + str(resp.status_code) + "\n \n \n"
            else:
                succDel = "DELETE request " + _url + _orders + " succesful"
                print succDel
                deltime = mes_api.get_time(resp.status_code) 
                print deltime

                # Send email notification
                lal = "Order " + str(_id) + " completed. \n \n Total score: \n" + str(mes_api.global_score) + " boxes. \n" + "\n"
                delBody = succDel + "\n" + "\n" + lal + deltime
                print delBody
                #feedback_api.mail_feedback(putSub, delBody)                

                # POST Log entry indicating deletion of the complete order
                r4 = mes_api.post_log(_url, _log, cell_id, cmnt, events_dict[8])
                if r4.status_code != 200:
                    print "Raised API Error on POST request. Status code " + str(r4.status_code)
                else:
                    print "POST request " + _url + _log + " succesful"
                    r4time = mes_api.get_time(r4.status_code)
                    print r4time
                    print "\n \n \n \n"


# Never ending loop