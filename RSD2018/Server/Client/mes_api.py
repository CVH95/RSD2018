#!/usr/bin/python

import requests
import time
import pymysql.cursors
import pymysql

# Robot System Design 2018 - SDU
# API of the project's MES System

# Print current timestamp
def get_time(stcode):
    print "On " + time.strftime("%c") + " - Status code = " + str(stcode) + "\n"

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
    print "Posted new log entry:"
    print "  >> cell_id: " + str(cid)
    print "  >> event: " + evt
    print "  >> cmnt: " + cmnt
    pst_url = _url + path
    return requests.post(pst_url, json=log)

# Delete an order (DELETE)
def delete_order(_url, path, d):
    _idd = '/' + str(d)
    d_url = _url + path + _idd
    return requests.delete(d_url) 