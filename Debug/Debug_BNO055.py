"""
 Description:
     
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Fri Jun  2 01:37:29 2017
"""
#==============================================================================
# START CODE
# BNO055 is an IMU measure absolute orientation.
# Connection to BBB
# Vin to 3.3 V on BBB
# GND to GND on BBB
# SDA to P9_20 on BBB, I2C2_SDA
# SCL to P9_19 on BBB, I2C2_SCL
# RST: Reset pin to P9_12 on BBB
# git clone 
# git clone https://github.com/adafruit/Adafruit_Python_BNO055.git
# Run the setup.py to install the Adafruit_BNO055 module.

import os,sys,inspect, logging
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from time import sleep
from sensors import *
from Adafruit_BNO055 import BNO055
#==============================================================================
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
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro)) 
print('Reading BNO055 data, press Ctrl-C to quit...')

#while(1):
#    heading, roll, pitch = bno.read_euler()
#    print('Heading: %.2f; Roll: %.2f; Pitch: %.2f') %(heading,roll,pitch)
#    sleep(1)