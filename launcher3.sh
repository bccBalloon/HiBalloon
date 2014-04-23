#!/bin/bash
# launcher1.sh
#navigate to home direction, then to this directory, then execute python script, then back home

exec &> capture.txt
sleep 30
cd /
cd root
dhclient
cd /
