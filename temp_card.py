#Written for the 135-102DAG-J01 Thermistor
import Adafruit_BBIO.ADC as ADC
import time
import datetime
import math as mt
ADC.setup()

#See June 4 comment on http://ealmberg.blogspot.com/2015/06/4-june-15.html

f1 = open('/media/CARD/temp2.csv', 'a')
f1.write("Month,Day,Hour,Minute,Second,Kelvin,Celsius,Fahrenheit\n")
Bvalue = 3348  #Beta
Ro = 1000      #Resistance at 25 C - room temperature
To = 298.15    #Room temperature Kelvin

while 1 :
   now = datetime.datetime.now()
   adcValue =  ADC.read("P9_37")
   R = Ro/((1/adcValue) - 1)  #Get measured resistance
   T = 1.0/To + (1.0/Bvalue)*mt.log(R/Ro)  #Formula from above blogspot address

   t_k = 1.0/T  #Temperature in Kelvin 
   print str(1.0/T) + 'K'  
   t_c = 1.0/T - 273.15   #Convert to celsius
   print str(t_c) + 'C'
   t_f = t_c*(9/5.0) + 32.0  #Convert to Fahrenheit
   print str(t_f) + 'F'
   #print str(adcValue) +', ' + str(1/adcValue) + ', ' + str(1/adcValue - 1) + ', ' + str(R)
   #print unichr(176)
   #print u"\u00B0"
   f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(t_k)+','+str(t_c)+','+str(t_f)+'\n');
   time.sleep(1)

f1.close()