# -*- coding: utf-8 -*-
"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Wed May 24 15:10:16 2017
"""
# Description:
#==============================================================================
# START CODE
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from timer import sleep
from bbio import *
#%%
#==============================================================================
# Digital Output
# Blink LED
# Pinout Ref
# https://graycat.io/beaglebone/beaglebone-pinout/
#==============================================================================
digOutPin = GPIO1_17 #'P9_23'
pinMode(digOutPin, OUTPUT)
for i in range(0,5): # Blink LED for 5 times
    digitalWrite(digOutPin, HIGH)
    sleep(0.5)
    digitalWrite(digOutPin, LOW)
    sleep(0.5)
#%%
#==============================================================================
# Digital Input, 1kOhm register pull down
#==============================================================================
digInPin = GPIO0_19 #'P9_27'    
pinMode(digInPin, INPUT)
count = 0
while(1):
    print "count: %d" %count
    count = count + 1
    if digitalRead(digInPin):
        print "Button Pressed"            
    if count == 10:
        break
    sleep(1)