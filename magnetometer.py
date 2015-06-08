from Adafruit_I2C import Adafruit_I2C

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


