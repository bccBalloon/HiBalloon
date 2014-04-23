import Adafruit_BBIO.ADC as ADC
import time
import datetime

#For reading analog data
ADC.setup()

f1 = open('pressure.csv','w')
f1.write("Month,Day,Hour,Minute,Second,Raw Pressure, Pressure (Hg)\n")


while 1 :
    now = datetime.datetime.now()
    raw =  ADC.read("P9_39")
    #convert raw voltage to pressure in Hg - formula derived from data sheet, page 11: http://sensing.honeywell.com/index.php?ci_id=151133
    p = ((raw * 1.8 * 2 -.33)/1.65)*29.92

    print str(raw) + ' ' + str(p)
    #write to csv file
    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(raw)+','+str(p)+'\n') 
    time.sleep(1)
f1.close()

