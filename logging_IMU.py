"""
 Description:
     
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Mon Jun  5 00:58:46 2017
"""
#==============================================================================
# START CODE
# Hardware setup. BNO055 connection to BBB.
# Vin to 3.3 V on BBB
# GND to GND on BBB
# SDA to P9_20 on BBB, I2C2_SDA
# SCL to P9_19 on BBB, I2C2_SCL
# RST: Reset pin to P9_12 on BBB
# Pinout Ref: https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/pinouts
from sensors import *
from Adafruit_BNO055 import BNO055
import uh_utils as uh
import time
#==============================================================================
# Hardware setup
rst_pin = 'P9_12'
bno = BNO055.BNO055(rst = rst_pin)
# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.') 
# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
# FileIO setup
myFile = uh.FileIO(logfilekey = ['IMU'])
myFile.make_expfiles()
txtheader = 'Time \t Acc_x \t Acc_y \t Acc_z \t Heading \t Roll \t Pitch \n'
myFile.logfile['IMU'].write(txtheader)
timer = time
start = timer.time()
print 'START: IMU data collection!'
try:
    while(1):
        timelog = timer.time() - start
        accx, accy, accz = bno.read_linear_acceleration()
        heading, roll, pitch = bno.read_euler()
        myFile.logfile['IMU'].write('%.3f \t %.2f \t %.2f \t %.2f \t %.2f \t %.2f \t %.2f \t \n' \
                                    %(timelog,accx, accy, accz,\
                                      heading,roll,pitch))
except KeyboardInterrupt:
    myFile.logfile['IMU'].close()
    print 'EXIT: Data collection completed!'
