from pynmea import nmea

f1 = open('gps.csv','r')
f2 = open('gps_derived.csv', 'w')
count = 0
count_GPGGA = 0
count_GPRMC = 0
for gps_line in f1:
	count += 1
	if "$GPGGA" in gps_line:
		count_GPGGA += 1
		continue
	if(gps_line.startswith('$GPRMC')):		
		gprmc = nmea.GPRMC()	
		gprmc.parse(gps_line)
		try:
			if gprmc.data_validity != 'A':
				continue
			s_d = str(gprmc.datestamp)
			if '06' not in s_d:
				continue
			d = s_d[0:2]+'/'+s_d[2:4]+'/20'+s_d[4:6]
			s_t = str(gprmc.timestamp)
			t =  s_t[0:2]+':'+s_t[2:4]+':'+s_t[4:6]+':'+s_t[7:10] + ' UTC'
			latitude = str(gprmc.lat)
			longitude = str(gprmc.lon)
			lat_dir = str(gprmc.lat_dir)
			lon_dir = str(gprmc.lon_dir)
			speed = str(gprmc.spd_over_grnd)
			true_course = str(gprmc.true_course)	
		except Exception as err:
			print(err)
		try: 
			write_line = d + ',' + t + ',' + latitude + ',' +  lat_dir + ','  + longitude + ','  + lon_dir + ',' + speed + ',' + true_course +'\n'
			f2.write(write_line)
			count_GPRMC += 1
		except Exception as err:
			print(err)


print "GPGGA lines: " +str(count_GPGGA)
print "GPRMC lines: " + str(count_GPRMC)
print "Loop count: " + str(count)
f1.close()
f2.close()
