#!/bin/bash

var1=$(hostname -I) 
echo "Your IPs are:  $var1"
route
echo "   "
cd /home/pi/Workspace/RSD2018/RSD2018/Client_rpi_version
echo "Initializing Workcell 3"
python3 mes_client.py "$var1"