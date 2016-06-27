import Adafruit_BBIO.ADC as ADC
import time
import datetime

ADC.setup()

soundPin = "P9_33"

cycles = 20


f1 = open('sound.csv', 'a')
f2 = open('rawSound.csv', 'a')
f1.write("Minimum,Maximum,Peak to Peak")
f1.write('\n')
f2.write("Minimum,Maximum,Peak to Peak")
f2.write('\n')

while 1:
	try :
		peakToPeak = 0
		raw = []
		for x in xrange(0,cycles) :
			raw.append(ADC.read(soundPin))		
			time.sleep(1/cycles)
		min_v = min(raw) * 3.3
		max_v = max(raw) * 3.3
		print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		print "min " + str(min_v)
		print "max " + str(max_v)
		peakToPeak = max_v - min_v;  # max - min = peak-peak amplitude
		print peakToPeak		
		f1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' UTC'+','+str(min_v)+','+str(max_v)+','+str(peakToPeak))
		f1.write('\n')
		f2.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' UTC'+','+str(min(raw))+','+str(max(raw))+','+str(max(raw)-min(raw)))
		f2.write('\n')
		print "Dataproint"
	except Exception as err :
		print 'Error:', err
	time.sleep(1)
f1.close()
