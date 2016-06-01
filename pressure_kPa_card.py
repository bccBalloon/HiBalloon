#!/usr/bin/env python
import Adafruit_BBIO.ADC as ADC
import time
import datetime

ADC.setup()

while 1:
  try:
    f1 = open('/media/CARD/pressure.csv', 'a')
    if not f1.closed:
      f1.write("Month,Day,Hour,Minute,Second,p,rawP\n")
      break
  except Exception as error1:
    print 'Error ' + str(error1)
    time.sleep(1)

while 1:
  now = datetime.datetime.now()
  rawP =  ADC.read("P9_39")
  p = ((rawP * 1.8 * 2 -.33)/1.65)*100
  print str(rawP) + ' ' + str(p)
  try:
    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(p)+','+str(rawP)+'\n')
    time.sleep(1)
  except Exception as error2:
    print 'Error ' + str(error2)

try:
  f1.close()
  if f1.closed:
    pass
except Exception as error3:
  print 'Error ' + str(error3)