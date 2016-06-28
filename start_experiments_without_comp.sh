#!/bin/bash


nohup python gps_raw.py &
nohup python pressure_kPa.py &
nohup python pressure_kPa_card.py &
nohup python temp.py &
nohup python temp_card.py &
nohup python extTemp.py &
nohup python extTemp_card.py &
nohup python accel.py &
nohup python accel_card.py &