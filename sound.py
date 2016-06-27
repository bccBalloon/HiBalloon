import Adafruit_BBIO.ADC as ADC
import time

ADC.setup()

soundPin = "P9_33"

cycles = 20

f1 = open('sound.csv', 'a')
f1.write("Minimum,Maximum,Peak to Peak")



while 1:
	peakToPeak = 0
	raw = []
	for x in xrange(0,cycles) :
		raw.append(ADC.read(soundPin))		
		time.sleep(1/cycles)
	min_v = min(raw) * 3.3
	max_v = max(raw) * 3.3
	print "min " + str(min_v)
	print "max " + str(max_v)
        peakToPeak = max_v - min_v;  # max - min = peak-peak amplitude
        print peakToPeak
        f1.write('\n')
	f1.write(str(min_v)+','+str(max_v)+','+str(peakToPeak))
	print "Dataproint"
	time.sleep(1)
f1.close()