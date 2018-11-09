#!/usr/bin/python
# Testing POST requests sent to rsd_2018_app.py

import requests

# Dictionary for the task
log = {"cell_id": 3, "comment": "Carlos logs 4.0", "event": "PML_Held"}

print('POST request into RSD server in http://localhost:5000/ \n')
print('The following log was posted: "cell_id: 3, comment: Carlos logs 4.0, event: PML_Held"')

# POST new task
resp = requests.post('http://localhost:5000/log', json=log)

# On success, status code is 201
#if resp.status_code != 201:
    #raise ApiError('POST /tasks/ {}'.format(resp.status_code))
print('Status code: ', resp.status_code)

print('Log entry was succesfully added. Refresh the browser to see it on the server.')

## UP UNTIL HERE IT IS CORRECT

# Print created task credentials
#print('New log entry from cell: {}'.format(resp.json()['cell_id']))
#print('with the following comment: {}'.format(resp.json()['comment']))
#print('and event type: {}'.format(resp.json()['event']))
#print('\n')