# -*- coding: utf-8 -*-
"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Wed May 24 15:23:25 2017
"""
#==============================================================================
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from timer import sleep
from sensors import *
#==============================================================================
data_pin = GPIO1_15  # P8.15
clk_pin  = GPIO1_14  # P8.16 Has to be a CLK Pin?
cs_pin   = GPIO0_27  # P8.17. 
myencoder = SPIencoder(data_pin, clk_pin, cs_pin,10)
digInPin = GPIO3_16 #'P9_30'  
DigInPinBreak = GPIO3_19 #'P9_27'    
digOutPin = GPIO1_17 #'P9_23'
pinMode(digInPin, INPUT)
pinMode(digInPinBreak, INPUT)
pinMode(digOutPin, OUTPUT)
while(1):
    if digitalRead(digInPinBreak):
        print "STOP"
        break
    if digitalRead(digInPin):
        print "Button Pressed"            
        digitalWrite(digOutPin, HIGH) 
    else:
        digitalWrite(digOutPin, LOW) 
    print myencoder.readEncoder()
    sleep(0.1)    
