#Written for the 135-102DAG-J01 Thermistor
import Adafruit_BBIO.ADC as ADC
import time
import datetime
import math as mt

ADC.setup()

#See June 4 comment on http://ealmberg.blogspot.com/2015/06/4-june-15.html

Bvalue = 3348  #Beta
Ro = 1000      #Resistance at 25 C
To = 298.15    #Room temperature in Kelvin

# Make sure the out file is opened properly
while 1:
  try:
    f1 = open('/media/CARD/temp2.csv', 'a')
    f2 = open('/media/CARD/temp_errors2.csv', 'a')
    print "Successfully opened", f1.name
    print "Successfully opened", f2.name
    f1.write("Month,Day,Hour,Minute,Second,ADC,Resistance,Kelvin,Celsius,Fahrenheit\n")
    f2.write("Month,Day,Hour,Minute,Second,Error\n")
    break
  except Exception as error1:
    print 'Error ' + str(error1)
    time.sleep(1)

# Get thermistor values and write them to file
while 1:
  try:
    now = datetime.datetime.now()

    adcValue =  ADC.read("P9_37")
    R = Ro/((1/adcValue) - 1)  #Get measured resistance
    T = 1.0/To + (1.0/Bvalue)*mt.log(R/Ro)  #Formula from above blogspot address

    t_k = 1.0/T  #Temperature in Kelvin 
    print str(t_k) + 'K'  
    t_c = 1.0/T - 273.15   #Convert to celsius
    print str(t_c) + 'C'
    t_f = t_c*(9/5.0) + 32.0  #Convert to Fahrenheit
    print str(t_f) + 'F'

    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(adcValue)+','+str(R)+','+str(t_k)+','+str(t_c)+','+str(t_f)+'\n');
  except Exception as error2:
    print 'Error ' + str(error2)
    f2.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(error2)+'\n');
  time.sleep(1)

f1.close()
f2.close()