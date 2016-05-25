#!/usr/bin/env python
import Adafruit_BBIO.ADC as ADC
import time
import datetime

ADC.setup()

while 1:
        try:
                f1 = open('pressure.csv', 'a')
                if not f1.closed:
                        f1.write("Month,Day,Hour,Minute,Second,p,rawP\n")
                        break
        except Exception as error:
                print 'Error'

while 1:
   now = datetime.datetime.now()
   rawP =  ADC.read("P9_39")
   p = ((rawP * 1.8 * 2 -.33)/1.65)*100
   print str(rawP) + ' ' + str(p)
   f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minut$
   time.sleep(1)

f1.close()
