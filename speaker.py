import Adafruit_BBIO.PWM as PWM
import time

speakerPin = "P9_14"
PWM.start(speakerPin, 50, 3800, 1)
time.sleep(10)
PWM.stop(speakerPin)
