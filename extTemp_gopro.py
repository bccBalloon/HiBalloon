#Written for the 135-102DAG-J01 Thermistor
import Adafruit_BBIO.ADC as ADC
import time
import math as mt
import goprohero as gp
ADC.setup()

camera = gp.GoProHero('10.5.5.9', 'goprohero316')
cameraOn = False
recording = False
#See June 4 comment on http://ealmberg.blogspot.com/2015/06/4-june-15.html

Bvalue = 3348  #Beta
Ro = 1000      #Resistance at 25 C 
To = 298.15    #Room temperature Kelvin

while camera :
   adcValue =  ADC.read("P9_35")
   R = 1000/((1/adcValue) - 1)  #Get measured resistance
   T = 1.0/To + (1.0/Bvalue)*mt.log(R/Ro)  #Formula from above blogspot address
   T_K = 1.0/T
   if T_K > 301 and not cameraOn :
      cameraOn = camera.command('power', 'on')
      time.sleep(5)  
   print str(T_K) + ' K'  
   t_c = 1.0/T - 273.15   #Convert to celsius
   print str(t_c) + ' C'
   t_f = t_c*(9/5.0) + 32.0  #Convert to Fahrenheit
   print str(t_f)
   if T_K > 301 and cameraOn and not recording :
      recording = camera.command('record','on')
      time.sleep(2)
      
   elif T_K <= 301 and cameraOn and recording :
      recording =  not camera.command('record', 'off')
      time.sleep(2)
      cameraOn = not camera.command('power', 'sleep')
      time.sleep(5)    

   time.sleep(1)
