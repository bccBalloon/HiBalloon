import Adafruit_BBIO.ADC as ADC
import time
import datetime

#For reading analog data
ADC.setup()

f1 = open('pressure.csv','a')
f1.write("Month,Day,Hour,Minute,Second,Raw Pressure, Pressure (Hg)\n")


while 1 :
    now = datetime.datetime.now()
    rawP =  ADC.read("P9_39")
    #convert raw voltage to pressure in Hg - formula derived from data sheet, page 11: http://sensing.honeywell.com/index.php?ci_id=151133
    #p = ((rawP * 1.8 * 2 -.33)/1.65)*29.92
    #p = ((rawP * 1.8 * 2 -.33)/1.65)*100
    p = (1.6*(rawP*2.0*1.8-3.3*0.10))/(0.8*3.3)*100
    print str(rawP) + ' ' + str(p)
    #write to csv file
    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(rawP)+','+str(p)+'\n') 
    time.sleep(1)
f1.close()

