import Adafruit_BBIO.ADC as ADC
import time
import datetime
import numpy as np

ADC.setup()

# Based on observation of high and low raw readings X 3.6 V. Then took the average of each.
zeroOffsetZ = 1.672
zeroOffsetX = 1.595
zeroOffsetY = 1.614

#The sensitivity or conversion factor is the average for each axis minus low raw reading.
conversionFactorZ = 0.322
conversionFactorY = 0.325
conversionFactorX = 0.319

# For Thermistor
Bvalue = 3348  #Beta
Ro = 1000      #Resistance at 25 C 
To = 298.15    #Room temperature Kelvin

f1 = open('Data.csv','w')
f2 = open('rawData.csv','w');
f1.write("Month,Day,Hour,Minute,Second,Latitude,Longitude,Accel Z,Accel Y,Accel X,Int Temp,Ext Temp,Pressure,Sound,\n")
f2.write("Month,Day,Hour,Minute,Second,Latitude,Longitude,Accel Z,Accel Y,Accel X,Int Temp,Ext Temp,Pressure,Sound\n")

while 1 :
    now = datetime.datetime.now()
    # read accelerometer axes
    rawZ =  ADC.read("P9_40")
    rawY =  ADC.read("P9_38")
    rawX =  ADC.read("P9_36")
    rawT_int =  ADC.read("P9_37")  #Inside payload thermistor
    rawT_ext =  ADC.read("P9_37")  #External thermistor
    rawP =  ADC.read("P9_39")  # read pressure sensor
    
    #convert raw voltage to pressure Kpa - formula derived from data sheet, page 11: http://sensing.honeywell.com/index.php?ci_id=151133
    p = ((rawP * 1.8 * 2 -.33)/1.65)*100

    # Calculate Kelvin for internal thermistor
    R = 1000/((1/rawT_int) - 1)  #Get measured resistance
    T_int = 1.0/To + (1.0/Bvalue)*mt.log(R/Ro)  #Formula from above blogspot address
    T_int = 1.0/T_int
    
    # Calculate Kelvin for external thermistor
    R = 1000/((1/rawT_ext) - 1)  #Get measured resistance
    T_ext = 1.0/To + (1.0/Bvalue)*mt.log(R/Ro)  #Formula from above blogspot address
    T_ext = 1.0/T_ext
    
    # Calculate acceleration
    Zvalue = ((rawZ * 3.6) - zeroOffsetZ)/conversionFactorZ;
    Yvalue = ((rawY * 3.6) - zeroOffsetY)/conversionFactorY;
    Xvalue = ((rawX * 3.6) - zeroOffsetX)/conversionFactorX;
    
    # raw input is multiplied by 3.6 because it has to be multiplied by 1.8 to get voltage and since it is hooked up to a voltage
    # divider it also needs to be multiplied by 2 to get the original voltage
    
    #Below are the print statements used for debugging
    
    #print 'Z = '+str(Zvalue) + ' Y = ' + str(Yvalue) + ' X = ' + str(Xvalue);
    #a = np.array([Zvalue, Yvalue, Xvalue])
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
    
    f1.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+str(Zvalue)+','+str(Yvalue)+','+str(Xvalue)+','+str(T_int)+'\n'+str(T_ext)+'\n'+str(p)+'\n')     
    f2.write(str(now.month)+','+str(now.day)+','+str(now.hour)+','+str(now.minute)+','+str(now.second)+','+ str(rawZ)+','+str(rawY)+','+str(rawX)+'\n'+str(rawT_int)+'\n'+str(rawT_ext)+'\n'+str(rawP)+'\n');
    
    time.sleep(1)

f1.close()
f2.close()