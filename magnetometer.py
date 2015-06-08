from Adafruit_I2C import Adafruit_I2C
from time import sleep

mag_read_addr = 0x3D
mag_write_addr = 0x3C

# Addresses for reading x,y,z axes of the magnotomer. They are stored in registers and read as most significant bits (msb) and least significan bits (lsb).
# See page 11:
#http://www51.honeywell.com/aero/common/documents/myaerospacecatalog-documents/Defense_Brochures-documents/HMC5883L_3-Axis_Digital_Compass_IC.pdf

X_msb = 0x03
X_lsb = 0x04
Z_msb = 0x05
Z_lsb = 0x06
Y_msb = 0x07
Y_msb = 0x08


i2c_read = Adafruit_I2C(mag_read_addr)
i2c_write = Adafruit_I2C(mag_write_addr)


while 1:
   b_X = i2c_read.readS8(X_msb)
   s_X = i2c_read.readU8(X_lsb)
   b_Z = i2c_read.readS8(Z_msb)
   s_Z = i2c_read.readU*(Y_lsb)
   b_Y = i2c_read.readS8(Y_msb)
   s_Y = i2c_read.readU8(Y_lsb)   

   raw_X = b_X * 256 + s_X
   raw_Z = b_Z * 256 + s_Z
   raw_Y = b_Y * 256 + s_Y

   sleep(1.0)
