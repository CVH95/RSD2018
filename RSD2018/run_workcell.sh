#!/bin/bash

var1=$(hostname -I) 
echo "Your IP is:  $var1"
cd /home/pi/Workspace/RSD2018/RSD2018/Client_rpi_version
echo "Testing connectivity to MES system and PLC..."
# Run connectivity test
python3 initia.py "$var1"
cat ../genfiles/conn_status.txt
echo "Initializing Workcell 3"
# Conditional to check the output of the test and run WorkCell
