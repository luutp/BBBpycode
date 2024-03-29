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

from time import sleep
from sensors import *
#==============================================================================
cs_pin   = "P9_11"  # P8.17. 
clk_pin  = "P9_13"  # P8.16 Has to be a CLK Pin?
data_pin = "P9_15"  # P8.15
mysensor = SPIencoder(cs_pin, clk_pin, data_pin,10)
print mysensor
while(1):
    print mysensor.read_angle()
    sleep(1)
    
