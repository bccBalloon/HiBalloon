import Adafruit_BBIO.UART as UART
import serial
import time
#from time import gmtime, strftime
import datetime
from pynmea import nmea
 
f1 = open('gps.csv','a')

UART.setup("UART2")

ser = serial.Serial(port = "/dev/ttyO2", baudrate=57600)
ser.close()
ser.open()
if ser.isOpen():
	print "Serial is open!"
	while 1:
		try :
			gps = ser.readline()
			#print gps
		except OSError:
			print(err)
		if(gps.startswith('$GPRMC')):		
			gprmc = nmea.GPRMC()	
			gprmc.parse(gps)
		if(gps.startswith('$GPGGA')):		
			gpgga = nmea.GPGGA()	
			gpgga.parse(gps)
			#print gps
			#f1.write(gps)
			#f1.write('\n')
		try:
			print "Timestamp: " + gprmc.timestamp
		#	print datetime.datetime.fromtimestamp(float(gprmc.timestamp)).strftime('%Y-%m-%d %H:%M:%S')
		#	f1.write(gprmc)

		#	f1.write(datetime.datetime.fromtimestamp(float(gprmc.timestamp)).strftime('%H:%M:%S'))
		except Exception as err:
			print(err)
		try:
			print "Datestamp: " + gprmc.datestamp
		except Exception as err:
			print "Datestamp Error: " + str(err)
		try:
			print "Latitude: " + gprmc.lat
		except Exception as err:
			print "Latitude Error: "+ str(err)
		try:
			print "Latitude Direction: " + gprmc.lat_dir
		except Exception as err:
			print "Latitude Direction Error: " + str(err)
		try:
			print "Longitude: " + gprmc.lon
		except Exception as err:
			print "Longitude Error: " + str(err)
		try:
			print "longitude Direction: " + gprmc.lon_dir
		except Exception as err:
			print "Longitude Direction Error: " + str(err)
		try:
			print "Speed over ground: " + gprmc.spd_over_grnd
		except Exception as err:
			print "Speed over ground error: "+ str(err)
		try:
			print "True Course: " + gprmc.true_course
		except Exception as err:
			print "True Course Error: " + str(err)
		try:
			print "Altitude above sea level: " + gpgga.antenna_altitude + ' ' + gpgga.altitude_units +'\n'
		except Exception as err:
			print(err)
#			f1.write('\n')
#			f1.write(datetime.datetime.fromtimestamp(float(gprmc.datestamp)).strftime('%Y-%m-%d'))
#			f1.write('\n')
		#print time.time(gprmc.timestamp)
#			d = datetime.timedelta(gprmc.timestamp)
#			print "Datestamp: " + gprmc.datestamp
		
		try:
			print "Time: " +  datetime.datetime.fromtimestamp(float(gprmc.timestamp)).strftime('%H:%M:%S:%f')
		except Exception as err:
			print("Time error: " + str(err))

			#print "Latitude: " + gprmc.lat + gprmc.lat_dir
			#print "Longitude: " + gprmc.lon +gprmc.lon_dir
#			print "Speed: " + gprmc.spd_over_grnd
#			print "True Course: " + gprmc.true_course
#			print "Data validity: " + gprmc.data_validity

#			print "System Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
 #                       f1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
  #                      f1.write('\n')
 
		time.sleep(1)

#                if(gps.startswith('$GPGGA')):
#			gpgga = nmea.GPGGA()
#                        gpgga.parse(gps)
#			print "Printing GPGGA"
#                        print gps
#                        f1.write(gps)
#			f1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
#                        #print "Altitude: " + gpgga.alt
#			time.sleep(1)
#			gps.startswith("$GPZDA")
#			gpzda = nmea.GPZDA()
#			gpzda.parse(gps)
#			print "$GPZDA Timestamp: " + gpzda.timestamp
#			time.sleep(1)
f1.close()
