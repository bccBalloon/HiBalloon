import Adafruit_BBIO.UART as UART
import serial
import time
from time import gmtime, strftime
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
			print gps
		except OSError:
			print(err)
		if(gps.startswith('$GPRMC')):		
			gprmc = nmea.GPRMC()	
			gprmc.parse(gps)
			#print gps
			f1.write(gps)
			#f1.write('\n')
			local_time = time.time() - 14400 #Add 3600 when DST changes
			try:
				print "Timestamp: " + gprmc.timestamp
				print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(local_time)) + ' DST'
			#	print datetime.datetime.fromtimestamp(float(gprmc.timestamp)).strftime('%Y-%m-%d %H:%M:%S')
			#	f1.write(gprmc)
	
			#	f1.write(datetime.datetime.fromtimestamp(float(gprmc.timestamp)).strftime('%H:%M:%S'))
			except Exception as err:
				print(err)
#			f1.write('\n')
#			f1.write(datetime.datetime.fromtimestamp(float(gprmc.datestamp)).strftime('%Y-%m-%d'))
#			f1.write('\n')
			#print time.time(gprmc.timestamp)
#			d = datetime.timedelta(gprmc.timestamp)
#			print "Datestamp: " + gprmc.datestamp
			
			try:
                        	print "Date: " +  datetime.datetime.fromtimestamp(float(gprmc.datestamp)).strftime('%Y-%m-%d')
			except Exception as err:
				print(err)

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