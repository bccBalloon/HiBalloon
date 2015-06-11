import Adafruit_BBIO.ADC as ADC
import time
import datetime
import math

ADC.setup()
#zeroOffset Calculated with 100 kOhm resistor
#zeroOffset = 1.466
#zeroOffset for 470 K Ohm
#zeroOffset = 1.658

# Based on observation
zeroOffsetZ = 1.68
zeroOffsetX = 1.588
zeroOffsetY = 1.604


#From adxl335 data sheet - sensitivity is 300 mV/g
conversionFactor = 0.314;

f1 = open('acceleration.csv','w')
f2 = open('rawAcceleration.csv','w');
f1.write("Month,Day,Hour,Minute,Second,Z,Y,X\n")
f2.write("Month,Day,Hour,Minute,Second,Zraw,Yraw,Xraw\n")

while 1 :
    now = datetime.datetime.now()
    rawZ =  ADC.read("P9_40")
    rawY =  ADC.read("P9_38")
    rawX =  ADC.read("P9_36")
   
    Zvalue = ((rawZ * 3.6) - zeroOffsetZ)/conversionFactor;
    Yvalue = ((rawY * 3.6) - zeroOffsetY)/conversionFactor;
    Xvalue = ((rawX * 3.6) - zeroOffsetX)/conversionFactor;
    
    # raw input is multiplied by 3.6 because it has to be multiplied by 1.8 to get voltage and since it is hooked up to a voltage
    # divider it also needs to be multiplied by 2 to get the original voltage
    #print 'Z = '+str(Zvalue) + ' Y = ' + str(Yvalue) + ' X = ' + str(Xvalue);
    #norm = math.sqrt(Zvalue * Zvalue + Yvalue * Yvalue + Xvalue * Xvalue);
    #print 'norm = ' + str(norm);
    print 'Zraw = ' + str(rawZ * 3.6) + ' Yraw = ' + str(rawY * 3.6) + ' Xraw = ' + str(rawX * 3.6);
    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(Zvalue)+','+str(Yvalue)+','+str(Xvalue)+'\n');
    f2.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+ str(rawZ)+','+str(rawY)+','+str(rawX)+'\n');
    time.sleep(1)
f1.close()
f2.close()

