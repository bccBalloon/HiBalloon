#!/usr/bin/env python
import Adafruit_BBIO.ADC as ADC
import time
import datetime

ADC.setup()

f1 = open('pressure.csv', 'a')
f2 = open('rawpressure.csv', 'a')
f1.write("Month,Day,Hour,Minute,Second,p\n")
f2.write("Month,Day,Hour,Minute,Second,rawP\n")

while 1:
   now = datetime.datetime.now()
   rawP =  ADC.read("P9_39")
   p = ((rawP * 1.8 * 2 -.33)/1.65)*100
   print str(rawP) + ' ' + str(p)
   f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(p)+'\n');
   f2.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(rawP)+'\n');
   time.sleep(1)

f1.close()
f2.close()
