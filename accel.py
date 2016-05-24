#!/usr/bin/python

import Adafruit_BBIO.ADC as ADC
import time
import datetime
import numpy as np

ADC.setup()

# Based on observation of high and low raw readings X 3.6 V. Then took the average of each.
zeroOffsetX = 1.595
zeroOffsetY = 1.614
zeroOffsetZ = 1.672

#The sensitivity or conversion factor is the average for each axis minus low raw reading.
conversionFactorX = 0.319
conversionFactorY = 0.325
conversionFactorZ = 0.322

f1 = open('acceleration.csv','a')
f1.write("Month,Day,Hour,Minute,Second,Xraw,Yraw,Zraw,X,Y,Z\n")

while 1 :
    now = datetime.datetime.now()
    rawX =  ADC.read("P9_36")
    rawY =  ADC.read("P9_38")
    rawZ =  ADC.read("P9_40")

    # Convert raw values to g values
    # Reference: http://beagleboard.org/support/BoneScript/accelerometer/
    Xvalue = ((rawX * 3.6) - zeroOffsetX)/conversionFactorX
    Yvalue = ((rawY * 3.6) - zeroOffsetY)/conversionFactorY
    Zvalue = ((rawZ * 3.6) - zeroOffsetZ)/conversionFactorZ
    
    # raw input is multiplied by 3.6 because it has to be multiplied by 1.8 to get voltage and since it is hooked up to a voltage
    # divider it also needs to be multiplied by 2 to get the original voltage
    # Debug     print 'X =', str(Xvalue), 'Y =', str(Yvalue), 'Z =', str(Zvalue)
    a = np.array([Xvalue, Yvalue, Zvalue])
    # Debug     print 'Norm =', str(np.linalg.norm(a))
    # Debug     print 'Xraw =', str(rawX * 3.6), 'Yraw =', str(rawY * 3.6), 'Zraw =', str(rawZ * 3.6)
    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(rawX)+','+str(rawY)+','+str(rawZ)+','+str(Xvalue)+','+str(Yvalue)+','+str(Zvalue)+'\n')
    time.sleep(1)

f1.close()