import Adafruit_BBIO.UART as UART
import serial
from pynmea import nmea
 
UART.setup("UART2")

ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
ser.close()
ser.open()
if ser.isOpen():
	print "Serial is open!"
	gps = ser.readline()
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
ser.close()

