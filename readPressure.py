import Adafruit_BBIO.ADC as ADC
import time
import datetime

ADC.setup()

f1 = open('pressure.csv','w')
f1.write("Month,Day,Hour,Minute,Second,Raw Pressure, Pressure (Hg)\n")


while 1 :
    now = datetime.datetime.now()
    raw =  ADC.read("P9_39")
    p = ((raw * 1.8 * 2 -.33)/1.65)*29.92

    print str(raw) + ' ' + str(p)
    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(raw)+','+str(p)+'\n') 
    time.sleep(1)
f1.close()

