# Testing POST requests sent to rsd_2018_app.py

#import json
import requests

# CREATE GET REQUEST
resp = requests.get('http://localhost:5000/log') # remember using HTTP and NOT!!!!!!! https

print('GET request from RSD server in http://localhost:5000/ \n')

# On success, status code is 200
#if resp.status_code != 200:     # This means something went wrong.    
    #raise ApiError('GET /log {}'.format(resp.status_code))
    #print('Raised API error with status code: ', resp.status_code)

# Print list of 'to do' items IDs and summaries.
for todo_item in resp.json():
    #print('{} {}'.format(todo_item['id'], todo_item['summary']))
    print('id: {}'.format(todo_item['id']))
    print('time: {}'.format(todo_item['time']))
    print('cell_id: {}'.format(todo_item['cell_id']))
    print('comment: {}'.format(todo_item['comment']))
    print('event: {}'.format(todo_item['event']))
    print('\n')