#Written for the 135-102DAG-J01 Thermistor
import Adafruit_BBIO.ADC as ADC
import time
import math as mt
ADC.setup()

#See June 4 comment on http://ealmberg.blogspot.com/2015/06/4-june-15.html

Bvalue = 3348  #Beta
Ro = 1000      #Resistance at 25 C 
To = 298.15    #Room temperature Kelvin

while 1 :
   adcValue =  ADC.read("P9_35")
   R = 1000/((1/adcValue) - 1)  #Get measured resistance
   T = 1.0/To + (1.0/Bvalue)*mt.log(R/Ro)  #Formula from above blogspot address
 
   print str(1.0/T) + ' K'  
   t_c = 1.0/T - 273.15   #Convert to celsius
   print str(t_c) + ' C'
   t_f = t_c*(9/5.0) + 32.0  #Convert to Fahrenheit
   print str(t_f)
   time.sleep(1)
