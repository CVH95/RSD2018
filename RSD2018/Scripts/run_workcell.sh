#!/bin/bash

var1=($(hostname -I)) 
var2=${var1[0]}
var3=${var1[1]}
route
cd /home/pi/Workspace/RSD2018/RSD2018/Client_rpi_version
rm start_time.txt
python3 mes_client.py "$var2" "$var3"
#cat start_time.txt
#cat stats.txt
