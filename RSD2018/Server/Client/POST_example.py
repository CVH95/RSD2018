#!/usr/bin/python
# Testing POST requests sent to rsd_2018_app.py

# Log entries are used to keep up with the score of the system.
# Each time that the PackML status changes, a new log entry has to be generated.
# When an order is started/completed, put the id of the order in the log comment.

import requests

cid = input("Enter WorkCell ID: ")
cidint = int(cid)
evt = raw_input("Event type: ")
cmt = raw_input("Comment log entry: ")


# Dictionary for the task
log = {"cell_id": cidint, "comment": cmt, "event": evt}

print('POST request into RSD server in http://localhost:5000/ \n')
print('A new log entry with the following contents was posted:')
print(' >> cell_id: ', cidint)
print(' >> comment: ', cmt)
print(' >> event: ', evt)

# POST new task
resp = requests.post('http://localhost:5000/log', json=log)

# On success, status code is 200
print('Status code: ', resp.status_code)
print('Log entry was succesfully added. Refresh the browser to see it on the server.')