#!/usr/bin/python
# Testing GET requests sent to rsd_2018_app.py

import requests

# CREATE GET REQUEST - requesting '/orders'
resp = requests.get('http://localhost:5000/event_types')

print('GET request for EVENT TYPES in RSD server in http://localhost:5000/ \n')

# On success, status code is 200
print(' >> Status code: ', resp.status_code)

# Print EVENTS
print(' >> Text: ', resp.text)
print(' >> JSON: ', resp.json)    