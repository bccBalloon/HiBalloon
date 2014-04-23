#!/usr/bin/env python
import Adafruit_BBIO.ADC as ADC
import time
import datetime

ADC.setup()

while 1:
   rawP =  ADC.read("P9_39")
   p = ((rawP * 1.8 * 2 -.33)/1.65)*100
   print str(rawP) + ' ' + str(p)
   time.sleep(1)
