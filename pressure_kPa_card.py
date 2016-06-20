#!/usr/bin/env python
import Adafruit_BBIO.ADC as ADC
import time
import datetime

ADC.setup()

while 1:
  try:
    f1 = open('/media/CARD/pressure2.csv', 'a')
    f2 = open('/media/CARD/pressure_errors2.csv', 'a')
    print "Successfully opened", f1.name
    print "Successfully opened", f2.name
    f1.write("Month,Day,Hour,Minute,Second,p,rawP\n")
    f2.write("Month,Day,Hour,Minute,Second,Error\n")
    break
  except Exception as error1:
    print 'Error ' + str(error1)
    time.sleep(1)

while 1:
  try:
    now = datetime.datetime.now()

    rawP =  ADC.read("P9_39")
    print 'Raw Pressure: ' + str(rawP)
    p = ((rawP * 1.8 * 2 -.33)/1.65)*100
    print 'Pressure: ' + str(p)

    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(p)+','+str(rawP)+'\n')
  except Exception as error2:
    print 'Error ' + str(error2)
    f2.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(error2)+'\n');
  time.sleep(1)

f1.close()
f2.close()
