#!/usr/bin/python

import requests
import time
import pymysql.cursors
import pymysql
import socket
import sys

# Robot System Design 2018 - SDU
# API of the project's MES System
# Carlos, Caroline, Daniel

# Global variables
global_score = int()
_nCycles = int()

# Print current timestamp
def get_time(stcode):
    tBody = "On " + time.strftime("%c") + " - Status code = " + str(stcode) + "\n"
    return tBody

# Get order list (GET)
def get_events(_url, evp):
    g_url = _url + evp
    return requests.get(g_url)

# Get order list (GET)
def get_orders(_url, path):
    g_url = _url + path
    return requests.get(g_url)

# Get single order (GET)
def get_single(_url, path, s):
    _ids = '/' + str(s)
    gs_url = _url + path + _ids
    return requests.get(gs_url)

# Take order (PUT)
def put_order(_url, path, x):
    _idx = '/' + str(x)
    pt_url = _url + path + _idx
    return requests.put(pt_url) 

# Sleeping 
def die(secs):
    time.sleep(secs)

# Get ticket from database
def get_ticket(_id):
    # Connect to database
    conn = pymysql.connect(host='localhost',
                           user='rsd',
                           password='rsd2018',
                           db='rsd2018',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with conn.cursor() as cursor:
            # Select ticket 
            select_stmt = "select id, ticket from rsd2018.jobs where id = %s"
            cursor.execute(select_stmt, _id)
            result = cursor.fetchone()
    finally:
            # Close connection
        conn.close()
    
    return result

# Log system state (POST)
def post_log(_url, path, cid, cmnt, evt):
    log = {"cell_id": cid, "comment": cmnt, "event": evt}
    print ("Posted new log entry:")
    print ("  >> cell_id: " + str(cid))
    print ("  >> event: " + evt)
    print ("  >> cmnt: " + cmnt)
    pst_url = _url + path
    return requests.post(pst_url, json=log)

# Delete an order (DELETE)
def delete_order(_url, path, id, ticket):
    body = {"ticket":ticket}
    _idd = '/' + str(id)
    d_url = _url + path + _idd
    return requests.delete(d_url, json=body)

# PLC communication during the processing of the order
def plc_control(sock, _plc, events, _url, _path, cid, cmt):
    
    # Instance to global score
    global global_score

    print ("Status: CONNECTED")# in http://" + server_address[0] + ":" + str(server_address[1]) + "/")

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
    
    # GET and PUT the order HERE

    # Prepair data
    d = str(_plc[0]) + ',' + str(_plc[1]) + ',' + str(_plc[2])
    print ("Sending the order over socket: " + d)
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
                printm ("Waiting for updates...")
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
                        evt = events[_state]
                        post_log(_url, _path, cid, cmt, evt)
                    
                break
            
            else:
                print ("Server's reply: " + str(rec))
                print ("An error ocurred while sending the order. Re-sending...")
                plc_control(sock, _plc, events, _url, _path, cid, cmt)
        else:
            print ("Did not receive anything after sending the order")    
    

class manager:

    def __init__(self, cid):
        self.workcell = cid
        print("WorkCell #" + str(cid))
    
    def __del__(self):
        global global_score
        global _nCycles
        file = open("stats.txt","w")
        file.write("Total number of cycles: " + str(_nCycles) + "\n")
        file.write("Total number of packed boxes: " + str(global_score) + "\n")
        file.write("WorkCell #" + str(self.workcell) + " shutdown \n")
        file.close()