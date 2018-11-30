#!/usr/bin/python

import mes_api
import feedback_api
import sys

# Robot System Design 2018 - SDU
# REST API Client of the project's MES System
# Group 3: Carlos, Caroline, Daniel.

print ("#########################################")
print ("##  WORKCELL #3 SYSTEM INITIALIZATION  ##")
print ("######################################### \n")

#Get args
_arg = sys.argv[1]
_ipOwn = str(_arg)

# Define url and paths
#_host = 'localhost'
_host = '192.168.100.200'
#_url = 'http://' + _host + ':5000' # Debug
_url = 'http://' + _host
_events = '/event_types'

# Define output file
fi = open("../genfiles/conn_status.txt", "w")

# MES test
resp = mes_api.get_events(_url, _events)
respSub = "WorkCell 3 initialization"
if resp.status_code != 200:
    err = "Raised API Error on GET request. Connection to MES server failed." + "\n" + "\n"
    errtime = mes_api.get_time(resp.status_code)
    errBody = err + errtime
    feedback_api.mail_feedback(respSub, errBody)
    fi.write("Unable to establish connection to MES Server \n")

else:
    _own = "Started MES WorkCell 3 manager on IP address: " + _ipOwn + "\n" + "\n"
    succ = "Tried GET request " + _url + _events + " succesful. \n \n System connected to the server." + "\n" + "\n"
    succtime = mes_api.get_time(resp.status_code)
    succBody = _own + succ + succtime
    #feedback_api.mail_feedback(respSub, succBody)
    print (succBody)
    fi.write("Connected to MES Server \n")
    

print (" \n \n --------------------------------------------------------------------------- \n \n")

# PLC test
    
fi.close()

