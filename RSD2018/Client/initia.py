#!/usr/bin/python

import mes_api
import feedback_api

# Robot System Design 2018 - SDU
# REST API Client of the project's MES System
# Group 3: Carlos, Caroline, Daniel.

print "#########################################"
print "##  WORKCELL #3 SYSTEM INITIALIZATION  ##"
print "######################################### \n"


# Define url and paths
_url = 'http://localhost:5000'
_events = '/event_types'

resp = mes_api.get_events(_url, _events)
respSub = "WorkCell 3 initialization"
if resp.status_code != 200:
    err = "Raised API Error on GET request. Connection to MES server failed." + "\n" + "\n"
    errtime = mes_api.get_time(resp.status_code)
    errBody = err + errtime
    feedback_api.mail_feedback(respSub, errBody)

else:
    succ = "Tried GET request " + _url + _events + " succesful. \n \n System connected to the server." + "\n" + "\n"
    succtime = mes_api.get_time(resp.status_code)
    succBody = succ + succtime
    feedback_api.mail_feedback(respSub, succBody)

