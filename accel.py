import Adafruit_BBIO.ADC as ADC
import time
import datetime

ADC.setup()
#zeroOffset Calculated with 100 kOhm resistor
#zeroOffset = 1.466
#zeroOffset for 500 KOhm
zeroOffset = 1.647
#From adxl335 data sheet - sensitivity is 300 mV/g
conversionFactor = 0.300;

f1 = open('acceleration.csv','w')
f2 = open('rawAcceleartion.csv','w');
f1.write("Month,Day,Hour,Minute,Second,Z,Y,X\n")
f2.write("Month,Day,Hour,Minute,Second,Zraw,Yraw,Xraw\n")

while 1 :
    now = datetime.datetime.now()
    rawZ =  ADC.read("P9_40")
    rawY =  ADC.read("P9_38")
    rawX =  ADC.read("P9_36")
   
    Zvalue = ((rawZ * 3.6) - zeroOffset)/conversionFactor;
    Yvalue = ((rawY * 3.6) - zeroOffset)/conversionFactor;
    Xvalue = ((rawX * 3.6) - zeroOffset)/conversionFactor;
    # raw input is multiplied by 3.6 because it has to be multiplied by 1.8 to get voltage and since it is hooked up to a voltage
    # divider it also needs to be multiplied by 2 to get the original voltage
    print 'Z = '+str(Zvalue) + ' Y = ' + str(Yvalue) + ' X = ' + str(Xvalue);
    #print 'Zraw = ' + str(rawZ) + ' Yraw = ' + str(rawY) + ' Xraw = ' + str(rawX);
    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(Zvalue)+','+str(Yvalue)+','+str(Xvalue)+'\n');
    f2.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+ str(rawZ)+','+str(rawY)+','+str(rawX)+'\n');
    time.sleep(1)
f1.close()
f2.close()

