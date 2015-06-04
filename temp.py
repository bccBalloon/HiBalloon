import Adafruit_BBIO.ADC as ADC
import time
import math as mt
ADC.setup()

I = 1.520e-3
Bvalue = 3348
Ro = 1000
To = 298.15




while 1 :
   adcValue =  ADC.read("P9_36")
   R = 1000/((1/adcValue) - 1)
   T = 1.0/To + (1.0/Bvalue)*mt.log(R/Ro)
 
   print str(1.0/T) + ' K'
   t_c = 1.0/T - 273.15
   print str(t_c) + ' C'
   t_f = t_c*(9/5.0) + 32.0
   print str(t_f)
   time.sleep(1)
