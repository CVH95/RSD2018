#!/usr/bin/python
# Testing GET requests sent to rsd_2018_app.py

import requests

# CREATE GET REQUEST - requesting '/orders'
resp = requests.get('http://localhost:5000/orders')

print "GET request for ORDERS in RSD server in http://localhost:5000/ \n"

# On success, status code is 200
print " >> Status code: " + str(resp.status_code)
print "\n"

print " >> Json: \n"  
print resp.json()