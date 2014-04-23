from Adafruit_I2C import Adafruit_I2C
import time
import numpy as np
mag_addr = 0x1E

# Addresses for reading x,y,z axes of the magnotomer. They are stored in registers and read as most significant bits (msb) and least significan bits (lsb).
# See page 11:
#http://www51.honeywell.com/aero/common/documents/myaerospacecatalog-documents/Defense_Brochures-documents/HMC5883L_3-Axis_Digital_Compass_IC.pdf

config_register = 0x01
X_msb = 0x03
X_lsb = 0x04
Z_msb = 0x05
Z_lsb = 0x06
Y_msb = 0x07
Y_lsb = 0x08


i2c = Adafruit_I2C(mag_addr)
#i2c_read = Adafruit_I2C(mag_read_addr)
#i2c_write = Adafruit_I2C(mag_write_addr)

while 1:
    x = 0
    time.sleep(1)
    for x in xrange(0,10):
       Adafruit_I2C.write8(i2c, 0x00, 0x18) # 1 Average, 15 Hz, normal measurement
       Adafruit_I2C.write8(i2c, 0x01, 0x20) # Set Gain
       Adafruit_I2C.write8(i2c, 0x02, 0x00) # Continuous measurement
       x += 1
    z_l = Adafruit_I2C.readU8(i2c, Z_lsb)
    z_m = Adafruit_I2C.readS8(i2c, Z_msb)
    z = z_m << 8 | z_l
    z = z/2048.0 * 1.3
    
    y_l = Adafruit_I2C.readU8(i2c, Y_lsb)
    y_m = Adafruit_I2C.readS8(i2c, Y_msb)
    y = y_m << 8 | y_l
    y = y/2048.0 * 1.3

    x_l = Adafruit_I2C.readU8(i2c, X_lsb)
    x_m = Adafruit_I2C.readS8(i2c, X_msb)
    x = x_m << 8 | x_l
    x = x/2048.0 * 1.3

    a = np.array([x,y,z])
    print 'Norm = ' + str(np.linalg.norm(a));
    print x
    print y
    print z
