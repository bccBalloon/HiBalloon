import Adafruit_BBIO.ADC as ADC
import time

ADC.setup()

cycles = 10
soundPin = "P9_33"
raw = []
count = 10
n = 0

f1 = open(rawSound.csv, 'a')
f1.write("Minimum,Maximum")


while n < count:
	for x in xrange(0,cycles)
		raw.append(ADC.read(soundPin))		
		time.sleep(1/cycles)
	#print min(raw)
	#print max(raw)
	f1.write(str(min(raw))+','+str(max(raw)))
	print "datapoint"
	time.sleep(1)
	n++
f1.close()