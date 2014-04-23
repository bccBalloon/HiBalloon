import Adafruit_BBIO.UART as UART
import serial
import time
import datetime
from pynmea import nmea
 
UART.setup("UART2")

ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
ser.close()
ser.open()
if ser.isOpen():
	print "Serial is open!"
	while 1:
		gps = ser.readline()
		print gps
		if(gps.startswith('$GPRMC')):		
			gprmc = nmea.GPRMC()	
			gprmc.parse(gps)
			print gps
			print "Timestamp: " + gprmc.timestamp
			print "Datestamp: " + gprmc.datestamp
			print "Latitude: " + gprmc.lat + gprmc.lat_dir
			print "Longitude: " + gprmc.lon +gprmc.lon_dir
			print "Speed: " + gprmc.spd_over_grnd
			print "True Course: " + gprmc.true_course
			print "Data validity: " + gprmc.data_validity 
			time.sleep(1)

