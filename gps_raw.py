import Adafruit_BBIO.UART as UART
import serial
import time
import datetime
from pynmea import nmea

"""	NOTES: 

 -- The pynmea library creates NMEASentence classes whose attributes are parts of an nmea sentence.
	Since, at the time of this file being written, there is no documentation providing the attribute names,
	the next best place to look for these names would be in nmea.py from the pynmea library.
	Each child class assigns a two-dimensional tuple to parse_map. Within the outer tuple, each inner tuple
	contains two values: 1) a description of the attribute and 2) the attribute name. 
	Reference for nmea sentences: http://www.catb.org/gpsd/NMEA.html

 -- Unlike every other program, this one opens two files out of concern for the serial bus. If there were two programs
  	running at the same time and making use of UART2, the serial might become overloaded, causing the programs to fail
  	in reading the nmea sentences off the gps 

 -- This program will only work when two conditions are met: 1) the microSD card is mounted onto the beaglebone,
	and 2) the microSD card IS NOT set to read only. If the microSD card is locked you MUST unlock it by
	using the SD card adapter. 
	To unlock the card, see this post: http://bergenballoon.blogspot.com/2016/06/week-three-june-9-2016.html

"""

# Make sure the out file is opened properly
while 1:
    try:
        f1 = open('gps_raw.csv','a')	# open() can cause an IOError
        print "Successfully opened", f1.name
        break
    except Exception as err:
        print 'Error:', err
        time.sleep(1)

while 1:
    try:
        f2 = open('/media/CARD/gps_raw2.csv','a')	# open() --> IOError
        print "Successfully opened", f2.name
        break
    except Exception as err:
        print 'Error:', err
        time.sleep(1)

while 1:
	try:
		UART.setup("UART2")
		ser = serial.Serial(port = "/dev/ttyO2", baudrate=57600)	# serial.Serial() --> ValueError, SerialException
		break
	except Exception as err:
		print 'Error:', err
        time.sleep(1)

ser.close()
ser.open()

# Get nmea sentences from the gps and write them to file
if ser.isOpen():
	print "Serial is open!"
	time.sleep(1)
	while 1:
		try:
			gps = ser.readline()
			f1.write(str(datetime.datetime.now())+','+gps)
			f2.write(str(datetime.datetime.now())+','+gps)

			# If there is a second nmea sentence that cuts into the first (which happens frequently), use the second one
			if gps.find('$') != -1:
				dollar_signs = [i for i in range(len(gps)) if gps[i] == '$']
				gps = gps[dollar_signs[-1]:]

			if gps.startswith('$GPGGA'):	
				gga = nmea.GPGGA()	
				gga.parse(gps)
				print '\n---------- GPGGA ----------'
				print gps, 	# Each gps line ends with '\n'
				print "Timestamp (hhmmss.sss): " + gga.timestamp
				print "Latitude: " + gga.latitude + ' ' + gga.lat_direction
				print "Longitude: " + gga.longitude + ' ' + gga.lon_direction
				print "Altitude above sea level: " + gga.antenna_altitude + ' ' + gga.altitude_units
				print "GPS Quality: " + gga.gps_qual
				print "Satellites in view: " + gga.num_sats
				print '---------------------------'

			if gps.startswith('$GPRMC'):	
				gprmc = nmea.GPRMC()	
				gprmc.parse(gps)
				print '\n---------- GPRMC ----------'
				print gps,	# Each gps line ends with '\n'
				print "Datestamp (ddmmyy): " + gprmc.datestamp
				#print "Date: " +  datetime.datetime.fromtimestamp(float(gprmc.datestamp)).strftime('%Y-%m-%d')
				print "Timestamp (hhmmss.sss): " + gprmc.timestamp
				print "Latitude: " + gprmc.lat + ' ' + gprmc.lat_dir
				print "Longitude: " + gprmc.lon+ ' ' + gprmc.lon_dir
				print "Ground speed: " + gprmc.spd_over_grnd + ' knots', float(gprmc.spd_over_grnd)/0.868976, 'mph'
				print "True Course: " + gprmc.true_course
				print '---------------------------'

			# Print the time in reference to daylight savings 
			local_time = time.time() - 14400 #Add 3600 when DST changes
			# print "Timestamp(adjusted): " + gprmc.timestamp
			print "Date and time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(local_time)) + ' DST'

		except Exception as err:
			print "Error: " + str(err)

		time.sleep(1)
f1.close()
f2.close()