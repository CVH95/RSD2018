#!/bin/bash

var1=$(hostname -I)
var2=${var1[0]}
var3=${var1[1]} 
cd /home/pi/Workspace/RSD2018/RSD2018/Client_rpi_version
echo "Initializing test of connectivity. Make sure the Pi is connected to:"
echo "  >> RSD MES master on WiFi"
echo "  >> PLC on Ethernet"
echo "Showing routing tables:"
route
echo "   "
python3 initia.py "$var2" "$var3"