#!/usr/bin/python

import requests

def deletion(_url, path, id, ticket):
    body = {"ticket":ticket}
    _idd = '/' + str(id)
    d_url = _url + path + _idd
    return requests.delete(d_url, json=body)

_host = '192.168.100.200'
_url = 'http://' + _host
_order = '/orders'

_id = 849
_tk = 'EA4047'

resp = deletion(_url, _order, _id, _tk)
if resp.status_code != 200:
    print ("Raised API Error on DELETE request. Status code " + str(resp.status_code))
else:
    succDel = ("DELETE request " + _url + _order + " succesful")
    print (succDel)
