import Adafruit_BBIO.UART as UART
import serial
import time
import datetime
from pynmea import nmea
 
UART.setup("UART2")

ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
ser.close()
ser.open()
gpgll = nmea.GPGLL()
gprmc = nmea.GPRMC()
gpvtg = nmea.GPVTG()
gpgga = nmea.GPGGA()
gpgsa = nmea.GPGSA()
gpgsv = nmea.GPGSV()
t = 0;

if ser.isOpen():
	print "Serial is open!"
	while 1:
		gps = ser.readline()
		if(gps.startswith('$GPGLL')):
			gpgll.parse(gps)
		if(gps.startswith('$GPRMC')):
			gprmc.parse(gps)
			t = t+1
		if(gps.startswith('$GPVTG')):
			gpvtg.parse(gps)
		if(gps.startswith('$GPGGA')):
			gpgga.parse(gps)
		if(gps.startswith('$GPGSA')):
			gpgsa.parse(gps)
		if(gps.startswith('$GPGSV')):
			gpgsv.parse(gps)
			print "\n\nMinute: " + str(t/60) + " Second: " + str(t%60) + "\n\n"
			print "Latitude: " + gprmc.lat + gprmc.lat_dir
			print "Longitude: " + gprmc.lon + gprmc.lon_dir
			print "Altitude" + gpgga.antenna_altitude
			print "Speed: " + gprmc.spd_over_grnd
			print "True Course: " + gprmc.true_course
			print "GPS Quality: " + gpgga.gps_qual
			print "Number of Sats: " + gpgga.num_sats
			print "Number of Sats in view: " + gpgsv.num_sv_in_view			
			print "Age of GPS Data: " + gpgga.age_gps_data
			print "Fix 1= no fix 2= 2d fix 3= 3d fix: " + gpgsa.mode_fix_type




		
