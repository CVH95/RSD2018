#!/bin/bash

cd /home/charlie/Workspace/WebProgramming/RSD2018/RSD2018/plc_tests
while true; do
    python plc_fake_server.py
    echo " "
    sleep 1
    done