import Adafruit_BBIO.ADC as ADC
import time
import datetime

ADC.setup()
#zeroOffset Calculated with 100 kOhm resistor
zeroOffset = 1.466
#zerroOffset for 500 KOhm
#zeroOffset = 1.647
#From adxl335 data sheet - sensitivity is 300 mV/g
conversionFactor = 0.300;

#f1 = open('pressure.csv','w')
#f1.write("Month,Day,Hour,Minute,Second,Raw Pressure, Pressure (Hg)\n")


while 1 :
    now = datetime.datetime.now()
    rawZ =  ADC.read("P9_40")
    #rawY = ADC.read("P9_37")
    #rawX = ADC.read("P9_35")
    #p = ((raw * 1.8 * 2 -.33)/1.65)*29.92

    #print 'X='+str(rawX) + ' Y=' + str(rawY) + ' Z='+str(rawZ);
   
    Zvalue = ((rawZ * 3.6) - zeroOffset)/conversionFactor;
    # rawZ is multiplied by 3.6 because it has to be multiplied by 1.8 to get voltage and since it is hooked up to a voltage
    # divider it also needs to be multiplied by 2 to get the original voltage
    print 'Z='+str(Zvalue) #+' Z\'= ' +str(Zvalue); 
    #f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(raw)+','+str(p)+'\n') 
    time.sleep(1)
#f1.close()

