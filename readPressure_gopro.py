#!/usr/bin/env python
import Adafruit_BBIO.ADC as ADC
import goprohero as gp
import time
import datetime

#For reading analog data
ADC.setup()

camera = gp.GoProHero('10.5.5.9', 'goprohero316')
cameraOn = False
recording = False

f1 = open('pressure_gopro1.csv','a')
f1.write("Month,Day,Hour,Minute,Second,Raw Pressure,Pressure (kPa),Recording\n")


while 1 :
    now = datetime.datetime.now()
    rawP =  ADC.read("P9_39")
    #convert raw voltage to pressure in Hg - formula derived from data sheet, page 11: http://sensing.honeywell.com/index.php?ci_id=151133
    #p = ((raw * 1.8 * 2 -.33)/1.65)*29.92
    p = ((rawP * 1.8 * 2 -.33)/1.65)*100
    p = ((rawP * 1.8 * 2 -.33)/1.65)*100
    #print str(rawP) + ' ' + str(p)
    if p < 1.09 and not cameraOn :
       cameraOn = camera.command('power', 'on')
       time.sleep(5)

    if p < 1.09 and cameraOn and not recording :
       recording = camera.command('record','on')
       time.sleep(5)

    elif p >= 1.09 and cameraOn and recording :
       recording =  not camera.command('record', 'off')
       time.sleep(5)
       cameraOn = not camera.command('power', 'sleep')
       time.sleep(5)
    if recording :
       recordStr = "True"
    else :
       recordStr = "False"    
    #write to csv file
    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(rawP)+','+str(p)+','+recordStr+'\n') 
    time.sleep(1)
f1.close()

