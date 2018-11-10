#!/usr/bin/python
# Testing GET requests sent to rsd_2018_app.py

import requests

# GET request of an order by its ID: @app.route('/orders/<int:order_id>', methods=['GET'])
resp = requests.get('http://localhost:5000/orders/1')

print('GET request for ORDER with ID:1 in RSD server in http://localhost:5000/ \n')

# On success, status code is 200
print(' >> Status code: ', resp.status_code)

# Print order
print(' >> Text: ', resp.text)
#print(' >> JSON: ', resp.json)

# Testing PUT request to add new order into database.
    