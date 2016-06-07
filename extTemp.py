#Written for the 135-102DAG-J01 Thermistor
import Adafruit_BBIO.ADC as ADC
import time
import datetime
import math as mt

ADC.setup()

#See June 4 comment on http://ealmberg.blogspot.com/2015/06/4-june-15.html

Bvalue = 3348  		#Beta
Ro = 1000      		#Resistance at 25 C 
To = 298.15    		#Room temperature in Kelvin

# Make sure the out file is opened properly
while 1:
	try:
		outfile = open('externalTemp.csv','a')
		#raise IOError
		if not outfile.closed:
			print "Successfully opened", outfile.name
			outfile.write("Month,Day,Hour,Minute,Second,ADC,Resistance,Kelvin,Celsius,Fahrenheit\n")
			break
	except Exception as err:
		print 'Error:', err
		time.sleep(1)

# Get thermistor values and write them to file
while 1:
	try:
		now = datetime.datetime.now()

		adcValue =  ADC.read("P9_35")
		R = Ro/((1/adcValue) - 1)						#Get measured resistance
		kelvin = 1.0/To + (1.0/Bvalue)*mt.log(R/Ro)		#Formula from above blogspot address
		kelvin = 1.0/kelvin 			
		celsius = kelvin - 273.15 						
		fahrenheit = celsius*(9/5.0) + 32.0  			

		outfile.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(adcValue)+','+str(R)+','+str(kelvin)+','+str(celsius)+','+str(fahrenheit)+'\n')
		print str(kelvin) + 'K', str(celsius) + ' C', str(fahrenheit) + ' F'
	except Exception as err:
		print 'Error:', err

	time.sleep(1)

outfile.close()