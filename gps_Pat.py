import Adafruit_BBIO.UART as UART
import serial
import time
import datetime
from pynmea import nmea

"""	NOTE: 
	The pynmea library creates NMEASentence classes whose attributes are parts of an nmea sentence.
	Since, at the time of this file being written, there is no documentation providing the attribute names,
	the next best place to look for these names would be in nmea.py from the pynmea library.
	Each child class assigns a two-dimensional tuple to parse_map. Within the outer tuple, each inner tuple
	contains two values: 1) a description of the attribute and 2) the attribute name

	Reference for nmea sentences: http://www.catb.org/gpsd/NMEA.html
"""

# Make sure the out file is opened properly
while 1:
    try:
        f1 = open('gps_exception.csv','a')	# open() can cause an IOError
        if not f1.closed:
            print "Successfully opened", f1.name
            break
    except Exception as err:
        print 'Error:', err
        time.sleep(1)

UART.setup("UART2")
ser = serial.Serial(port = "/dev/ttyO2", baudrate=57600)
ser.close()
ser.open()

# Get nmea sentences from the gps and write them to file
if ser.isOpen():
	print "Serial is open!"
	while 1:
		try:
			gps = ser.readline()

			# If there is a second nmea sentence that cuts into the first (which happens frequently), use the second one
			another = gps[1:]
			if another.find('$') != -1:
				gps = another[another.find('$'):]

			if gps.startswith('$GPGGA'):		
				f1.write(gps)

				gga = nmea.GPGGA()	
				gga.parse(gps)
				print gps,
				print "GPS Quality: " + gga.gps_qual
				print "Satellites in view: " + gga.num_sats
				print "Timestamp: " + gga.timestamp
				print "Latitude: " + gga.latitude + ' ' + gga.lat_direction
				print "Longitude: " + gga.longitude + ' ' + gga.lon_direction
				print "Altitude above sea level: " + gga.antenna_altitude + ' ' + gga.altitude_units +'\n'

			if gps.startswith('$GPRMC'):		
				f1.write(gps)

				gprmc = nmea.GPRMC()	
				gprmc.parse(gps)
				print gps,
				# print "Timestamp: " + gprmc.timestamp
				print "Datestamp: " + gprmc.datestamp + '\n'
				"""
				print "Latitude: " + gprmc.lat + ' ' gprmc.lat_dir
				print "Longitude: " + gprmc.lon+ ' ' + gprmc.lon_dir
				print "Ground speed: " + gprmc.spd_over_grnd + ' knots'
				print "True Course: " + gprmc.true_course
				print "Date: " +  datetime.datetime.fromtimestamp(float(gprmc.datestamp)).strftime('%Y-%m-%d') + '\n'
				"""
			if gps.startswith('$GPVTG'):
				f1.write(gps)
				
				gpvtg = nmea.GPVTG()
				gpvtg.parse(gps)
				print gps,
				print "Ground speed: " + gpvtg.spd_over_grnd_kts + ' knots ' + gpvtg.spd_over_grnd_kmph + ' kmph\n'

			# Print the time in reference to daylight savings
			local_time = time.time() - 14400 #Add 3600 when DST changes
			# print "Timestamp(adjusted): " + gprmc.timestamp
			print "Date and time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(local_time)) + ' DST\n'
		except Exception as err:
			print "Error: " + str(err)

		time.sleep(1)
f1.close()