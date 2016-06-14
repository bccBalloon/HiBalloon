from pynmea import nmea
import datetime

start_time = datetime.datetime.now()

"""	NOTE: 
	The pynmea library creates NMEASentence classes whose attributes are parts of an nmea sentence.
	Since, at the time of this file being written, there is no documentation providing the attribute names,
	the next best place to look for these names would be in nmea.py from the pynmea library.
	Each child class assigns a two-dimensional tuple to parse_map. Within the outer tuple, each inner tuple
	contains two values: 1) a description of the attribute and 2) the attribute name

	Reference for nmea sentences: http://www.catb.org/gpsd/NMEA.html

	Using Python 2.7.10
"""

# Convert raw coordinates from degrees decimal minutes format to decimal degrees format. Return the result
# For reference, see http://bergenballoon.blogspot.com/2016/06/week-three-june-6-2016.html
def getDecimalDegrees(coordinate, direction):
	if not coordinate:
		return ''
	coor = float(coordinate)
	whole = float(int(coor/100))
	fraction = (coor-whole*100)/60
	coor = whole + fraction
	if direction == 'W' or direction == 'S':
		return str(-1.0 * coor)
	else:
		return str(coor)

# Return raw date and/or time that follows the string format
def getDateOrTime(format, timestamp, datestamp=None):
	time_num = float(timestamp)
	hour = int(time_num)/10000
	minute = (int(time_num) - hour*10000)/100
	second = int(time_num) - hour*10000 - minute*100
	microsecond = int((time_num - int(time_num))*1000000)
	microsecond = int(round(float(microsecond)/10)*10)	# corrects microsecond (i.e. 399999 is corrected to 400000).

	if datestamp is None:
		dt = datetime.time(hour, minute, second, microsecond)
	else:
		date_num = int(datestamp)
		day = date_num/10000
		month = (date_num - day*10000)/100
		year = (date_num - day*10000 - month*100) + 2000
		# print '%i/%i/%i' % (month, day, year),
		dt = datetime.datetime(year, month, day, hour, minute, second, microsecond)
	# print '%i:%i:%i.%i' % (hour,minute,second,microsecond)
	return dt.strftime(format)

# Write out data to files
with open('gps_raw_test.csv') as infile, open('gps_gga.csv', 'w') as outGGA, open('gps_rmc.csv', 'w') as outRMC, open('googleEarth.kml', 'w') as gEarth, open('googleMyMaps.csv', 'w') as myMaps, open('gps_errors.txt', 'w') as errors:
	outGGA.write('BeagleBone Black Date and Time UTC, Satellite Timestamp UTC,DDM Latitude,Latitude Direction,DDM Longitude,Longitude Direction,Altitude Above Sea Level (meters),GPS Quality,Satellites in View\n')
	outRMC.write('BeagleBone Black Date and Time UTC,Satellite Date and Time UTC,DDM Latitude,Latitude Direction,DDM Longitude,Longitude Direction,Raw Ground Speed (knots), Converted Ground Speed (mph),True Course\n')
	gEarth.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n<Style id="yellowPoly">\n<LineStyle>\n<color>7f00ffff</color>\n<width>4</width>\n</LineStyle>\n<PolyStyle>\n<color>7f00ff00</color>\n</PolyStyle>\n</Style>\n<Placemark>\n<styleUrl>#yellowPoly</styleUrl>\n<LineString>\n<extrude>1</extrude>\n<tesselate>1</tesselate>\n<altitudeMode>absolute</altitudeMode>\n<coordinates>\n')
	myMaps.write('BeagleBone Black Date and Time UTC,Satellite Timestamp UTC,DD Latitude,DD Longitude,Altitude Above Sea Level (meters)\n')

	error_count = 0
	for line in infile:
		try:
			# work on dt = datetime.datetime.strptime( line[:line.rfind('2016-')+26], '%Y-%m-%d %H:%M:%S.%f')
			dt = datetime.datetime.strptime( line[:line.find(',')], '%Y-%m-%d %H:%M:%S.%f')
			local_datetime = dt.strftime('%b %d %Y\t%H:%M:%S.%f')

			# If there is a second nmea sentence that cuts into the first (which happens frequently), use the second one
			# Assume that every nmea sentence has a '$' character
			gps = line[line.rfind('$'):]

			if gps.startswith('$GPGGA'):		
				gga = nmea.GPGGA()	
				gga.parse(gps)
				#print local_datetime + ',' + gps,
				outGGA.write(local_datetime + ',' + getDateOrTime('%H:%M:%S.%f', gga.timestamp) + ',' + gga.latitude + ',' + gga.lat_direction + ',' + gga.longitude + ',' + gga.lon_direction + ',' + gga.antenna_altitude + ',' + gga.gps_qual + ',' + gga.num_sats + '\n')
				
				if gga.latitude and gga.longitude and gga.antenna_altitude:
					gEarth.write('\t' + getDecimalDegrees(gga.longitude, gga.lon_direction) + ',' + getDecimalDegrees(gga.latitude, gga.lat_direction) + ',' + gga.antenna_altitude + '\n')
					myMaps.write(local_datetime + ',' + getDateOrTime('%H:%M:%S.%f', gga.timestamp) + ',' + getDecimalDegrees(gga.latitude, gga.lat_direction) + ',' + getDecimalDegrees(gga.longitude, gga.lon_direction) + ',' + gga.antenna_altitude + '\n')

			if gps.startswith('$GPRMC'):		
				rmc = nmea.GPRMC()	
				rmc.parse(gps)
				#print local_datetime + ',' + gps,
				outRMC.write(local_datetime + ',' + getDateOrTime('%b %d %Y\t%H:%M:%S.%f', rmc.timestamp, rmc.datestamp) + ',' + rmc.lat + ',' + rmc.lat_dir + ',' + rmc.lon + ',' + rmc.lon_dir + ',' + rmc.spd_over_grnd + ',' + str(float(rmc.spd_over_grnd)/0.868976) + ',' + rmc.true_course + '\n')
				
				# Should the rmc data be included to googleMyMaps.csv?
				#if rmc.lat and rmc.lon:
					#myMaps.write(local_datetime + ',' + getDateOrTime('%H:%M:%S.%f', rmc.timestamp) + ',' + getDecimalDegrees(rmc.lat, rmc.lat_dir) + ',' + getDecimalDegrees(rmc.lon, rmc.lon_dir) + '\n')

		except Exception as err:
			error_msg = 'Error occurred while reading: ' + line + '\tError: ' + str(err) + '\n'
			print error_msg
			errors.write(error_msg)
			error_count += 1
	gEarth.write('</coordinates>\n</LineString>\n</Placemark>\n</Document>\n</kml>')

print 'Number of faulty nmea sentences:', error_count
print 'Completed writing to files'
print 'Time elapsed:', (datetime.datetime.now() - start_time) 