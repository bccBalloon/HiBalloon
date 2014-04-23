import Adafruit_BBIO.ADC as ADC
import time

ADC.setup()

cycles = 360
soundPin = "P9_33"
raw = []
count = 0
n = 0
min = 1.0
max = 0.0

f1 = open("rawSound.csv", 'a')
#f1.write("Minimum,Maximum")


while count < 360:
	for x in xrange(0,cycles):
		count += 1
		current = ADC.read(soundPin)
		#raw.append(ADC.read(soundPin))
		time.sleep(1/cycles)
		#if current < min:
		#	min = current
		#if current > max:
		#	max = current
		f1.write(str(count)+','+str(current)+'\n')
	#print min(raw)
	#print max(raw)
        #print (str(min(raw))+','+str(max(raw)))
	print "datapoint"
	print str(min)+" , "+str(max)
	time.sleep(1)
	n+=1
	min = 1.0
	max = 0.0
#f1.close()
