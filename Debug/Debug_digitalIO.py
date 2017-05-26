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

from time import sleep
from bbio import *
#%%
#==============================================================================
# Digital Output
# Blink LED
# Pinout Ref
# https://graycat.io/beaglebone/beaglebone-pinout/
#==============================================================================
#digOutPin = GPIO1_17 #'P9_23'
#pinMode(digOutPin, OUTPUT)
#for i in range(0,5): # Blink LED for 5 times
#    print 'Flashing LED'
#    digitalWrite(digOutPin, HIGH)
#    sleep(0.5)
#    digitalWrite(digOutPin, LOW)
#    sleep(0.5)
#%%
#==============================================================================
# Digital Input, 1kOhm register pull down
#==============================================================================
digInPin = GPIO0_3 #'P9_17'    
pinMode(digInPin, INPUT)
count = 0
while(1):
    print "Press Button to stop. Waiting...: %d" %count
    count = count + 1
    if digitalRead(digInPin):
        print "Button Pressed"            
        break
    sleep(1)
#==============================================================================
# Test both digital input and output
#==============================================================================
#digInPin = GPIO3_19 #'P9_17'    
#digOutPin = GPIO1_17 #'P9_23'
#pinMode(digInPin, INPUT)
#pinMode(digOutPin, OUTPUT)    
#while(1):
#    print 'Flashing LED'
#    digitalWrite(digOutPin, HIGH)
#    sleep(0.5)
#    digitalWrite(digOutPin, LOW)
#    sleep(0.5)
#    if digitalRead(digInPin):
#        print "Button Pressed"            
#        break
