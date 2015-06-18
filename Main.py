import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.UART as UART
import time
import datetime
import numpy as np
import serial
from pynmea import nmea
from Adafruit_I2C import Adafruit_I2C

# Addresses for reading x,y,z axes of the magnotomer. They are stored in registers and read as most significant bits (msb) and least $
# See page 11:
#http://www51.honeywell.com/aero/common/documents/myaerospacecatalog-documents/Defense_Brochures-documents/HMC5883L_3-Axis_Digital_Co$

gprmc = nmea.GPRMC()
mag_addr = 0x1E
config_register = 0x01
X_msb = 0x03
X_lsb = 0x04
Z_msb = 0x05
Z_lsb = 0x06
Y_msb = 0x07
Y_lsb = 0x08

i2c = Adafruit_I2C(mag_addr)

UART.setup("UART2")

ser = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
ser.close()
ser.open()

ADC.setup()

# Based on observation of high and low raw readings of the accelerometer X 3.6 V. Then took the average of each.
zeroOffsetZ = 1.672
zeroOffsetX = 1.595
zeroOffsetY = 1.614

#The sensitivity or conversion factor is the average for each axis of the accelerometer minus low raw reading.
conversionFactorZ = 0.322
conversionFactorY = 0.325
conversionFactorX = 0.319

# Values off of the datasheet for Thermistor, to calculate temp
Bvalue = 3348  #Beta
Ro = 1000      #Resistance at 25 C 
To = 298.15    #Room temperature Kelvin

#create files and headers that we will save our data too
f1 = open('Data.csv','a')
f2 = open('rawData.csv','a');
f1.write("Datestamp,Timestamp,Latitude,Longitude,Speed,Course,Accel Z,Accel Y,Accel X,Accel Norm,Mag Z,Mag Y,Mag X,Mag Norm,Int Temp,Ext Temp,Pressure,Sound,\n")
f2.write("Datestamp,Timestamp,Latitude,Longitude,Speed,Course,Accel Z,Accel Y,Accel X,Mag Z,May Y,Mag X,Int Temp,Ext Temp,Pressure,Sound\n")

while 1 :

#   get gps data
    gps = ser.readline()
    while(not gps.startswith('$GPRMC')):        
       gps = ser.readline()    
    gprmc.parse(gps)

#   I2C code for reading the magnetometer
    counter = 0 
    for counter in xrange(0,10):            #send the commands several times to ensure Magnetometer receives the command 
       Adafruit_I2C.write8(i2c, 0x00, 0x18) # 1 Average, 15 Hz, normal measurement
       Adafruit_I2C.write8(i2c, 0x01, 0x20) # Set Gain
       Adafruit_I2C.write8(i2c, 0x02, 0x00) # Continuous measurement
       counter += 1
    z_l = Adafruit_I2C.readU8(i2c, Z_lsb)   #Data is stored in 2 registers on the chip, the Least significant and the
    z_m = Adafruit_I2C.readS8(i2c, Z_msb)   #most significant. Both must be read and the two combined into the actual number
    Zmag_raw = z_m << 8 | z_l
    Zmag = Zmag_raw/2048.0 * 1.3                      #Calculate Gauss value from the raw 12 bit number

    y_l = Adafruit_I2C.readU8(i2c, Y_lsb)   #rinse and repeat for each axis
    y_m = Adafruit_I2C.readS8(i2c, Y_msb)
    Ymag_raw = y_m << 8 | y_l
    Ymag = Ymag_raw/2048.0 * 1.3

    x_l = Adafruit_I2C.readU8(i2c, X_lsb)
    x_m = Adafruit_I2C.readS8(i2c, X_msb)
    Xmag_raw = x_m << 8 | x_l
    Xmag = Xmag_raw/2048.0 * 1.3

    mag_vector = np.array([Xmag,Ymag,Zmag])
#   print 'Norm = ' + str(np.linalg.norm(mag_vector));

#   read accelerometer axes, thermistors, and pressure sensor
    Zaccel_raw =  ADC.read("P9_40")
    Yaccel_raw =  ADC.read("P9_38")
    Xaccel_raw =  ADC.read("P9_36")
    rawT_int =  ADC.read("P9_37")  #Inside payload thermistor
    rawT_ext =  ADC.read("P9_37")  #External thermistor
    rawP =  ADC.read("P9_39")  # read pressure sensor
    
    #convert raw voltage to pressure Kpa - formula derived from data sheet, page 11: http://sensing.honeywell.com/index.php?ci_id=151133
    p = ((rawP * 1.8 * 2 -.33)/1.65)*100

    # Calculate Kelvin for internal thermistor
    R = 1000/((1/rawT_int) - 1)  #Get measured resistance
    T_int = 1.0/To + (1.0/Bvalue)*np.log(R/Ro)  #Formula from above blogspot address
    T_int = 1.0/T_int
    
    # Calculate Kelvin for external thermistor
    R = 1000/((1/rawT_ext) - 1)  #Get measured resistance
    T_ext = 1.0/To + (1.0/Bvalue)*np.log(R/Ro)  #Formula from above blogspot address
    T_ext = 1.0/T_ext
    
    # Calculate acceleration
    Zaccel = ((Zaccel_raw * 3.6) - zeroOffsetZ)/conversionFactorZ;
    Yaccel = ((Yaccel_raw * 3.6) - zeroOffsetY)/conversionFactorY;
    Xaccel = ((Xaccel_raw * 3.6) - zeroOffsetX)/conversionFactorX;
    
    # raw input is multiplied by 3.6 because it has to be multiplied by 1.8 to get voltage and since it is hooked up to a voltage
    # divider it also needs to be multiplied by 2 to get the original voltage

    #Below are the print statements used for debugging
    
    #print 'Z = '+str(Zvalue) + ' Y = ' + str(Yvalue) + ' X = ' + str(Xvalue);
    accel_vector = np.array([Zaccel, Yaccel, Xaccel])
    #print 'Norm = ' + str(np.linalg.norm(a));
    #print 'Zraw = ' + str(rawZ * 3.6) + ' Yraw = ' + str(rawY * 3.6) + ' Xraw = ' + str(rawX * 3.6);
    
    #Console print the calculated temperature
    #print str(T_int) + ' K'  
    #t_c = T_int - 273.15   #Convert to celsius
    #print str(t_c) + ' C'
    #t_f = t_c*(9/5.0) + 32.0  #Convert to Fahrenheit
    #print str(t_f)
    
    #print str(rawPressure) + ' ' + str(p)
    #write to csv file
    
    f1.write(gprmc.datestamp+','+gprmc.timestamp+','+gprmc.lat + gprmc.lat_dir+','+gprmc.lon + gprmc.lon_dir+','+gprmc.spd_over_grnd+','+gprmc.true_course+','+str(Zaccel)+','+str(Yaccel)+','+str(Xaccel)+','+str(np.linalg.norm(accel_vector))+','+str(Zmag)+','+str(Ymag)+','+str(Xmag)+','+str(np.linalg.norm(mag_vector))+','+str(T_int)+','+str(T_ext)+','+str(p)+'\n')     
    f2.write(gprmc.datestamp+','+gprmc.timestamp+','+gprmc.lat + gprmc.lat_dir+','+gprmc.lon + gprmc.lon_dir+','+gprmc.spd_over_grnd+','+gprmc.true_course+','+ str(Zaccel_raw)+','+str(Yaccel_raw)+','+str(Xaccel_raw)+','+ str(Zmag_raw)+','+str(Ymag_raw)+','+str(Xmag_raw)+','+str(rawT_int)+','+str(rawT_ext)+','+str(rawP)+'\n');
    print "datapoint"
    time.sleep(1)
f1.close()
f2.close()
