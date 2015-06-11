import Adafruit_BBIO.ADC as ADC
import time
import datetime
import numpy as np

ADC.setup()

# Based on observation of high and low raw readings X 3.6 V. Then took the average of each.
zeroOffsetZ = 1.672
zeroOffsetX = 1.595
zeroOffsetY = 1.614

#The sensitivity of conversion factor is the average for each axis minus low raw reading.
conversionFactorZ = 0.322
conversionFactorY = 0.325
conversionFactorX = 0.319

f1 = open('acceleration.csv','w')
f2 = open('rawAcceleration.csv','w');
f1.write("Month,Day,Hour,Minute,Second,Z,Y,X\n")
f2.write("Month,Day,Hour,Minute,Second,Zraw,Yraw,Xraw\n")

while 1 :
    now = datetime.datetime.now()
    rawZ =  ADC.read("P9_40")
    rawY =  ADC.read("P9_38")
    rawX =  ADC.read("P9_36")
   
    Zvalue = ((rawZ * 3.6) - zeroOffsetZ)/conversionFactorZ;
    Yvalue = ((rawY * 3.6) - zeroOffsetY)/conversionFactorY;
    Xvalue = ((rawX * 3.6) - zeroOffsetX)/conversionFactorX;
    
    # raw input is multiplied by 3.6 because it has to be multiplied by 1.8 to get voltage and since it is hooked up to a voltage
    # divider it also needs to be multiplied by 2 to get the original voltage
    print 'Z = '+str(Zvalue) + ' Y = ' + str(Yvalue) + ' X = ' + str(Xvalue);
    a = np.array([Zvalue, Yvalue, Xvalue])
    print 'Norm = ' + str(np.linalg.norm(a));
    #print 'Zraw = ' + str(rawZ * 3.6) + ' Yraw = ' + str(rawY * 3.6) + ' Xraw = ' + str(rawX * 3.6);
    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(Zvalue)+','+str(Yvalue)+','+str(Xvalue)+'\n');
    f2.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+ str(rawZ)+','+str(rawY)+','+str(rawX)+'\n');
    time.sleep(1)

f1.close()
f2.close()

