import Adafruit_BBIO.ADC as ADC
import time

ADC.setup()

cycles = 1000
soundPin = "AIN0"

f1 = open('rawSound.csv', 'w')
f1.write("Minimum,Maximum\n")


while 1:
        raw = []
        for x in xrange(0,cycles):
                raw.append(ADC.read(soundPin))
                time.sleep(1/cycles)
        print 'ADC Amplitude:',str(max(raw)-min(raw)), 'Volts:', (max(raw)-min(raw))*1.8
        f1.write(str(min(raw))+','+str(max(raw))+'\n')
        #time.sleep(1)
f1.close()