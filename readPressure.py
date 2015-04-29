import Adafruit_BBIO.ADC as ADC
import time
#import cv2

ADC.setup()

f1 = open('pressure.txt','a')

while 1 :
    raw =  ADC.read("P9_39")
    p = ((raw * 1.8 * 2 -.33)/1.65)*29.92
    print str(raw) + ' ' + str(p)
    f1.write(str(raw)+','+str(p)+'\n') 
    time.sleep(1)
f1.close()

