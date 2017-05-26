"""
 Description:
     
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Fri May 26 01:31:03 2017
"""
#==============================================================================
# START CODE

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import time
from sensors import *
import numpy as np
import uh_utils as uh
import matplotlib.pyplot as plt
#==============================================================================
cs_pin   = "P9_11"  # P8.17. 
clk_pin  = "P9_13"  # P8.16 Has to be a CLK Pin?
data_pin = "P9_15"  # P8.15
mysensor = SPIencoder(cs_pin, clk_pin, data_pin,10)
myfilter = uh.uh_filter(2,7,1000,'low')
raw_angle = []
filt_angle =[]
t = []
t_start = time.clock()
for i in range(20000):
    t.append(time.clock()-t_start)
    print 'Current time: %.3f' %(time.clock()-t_start)
    raw_angle.append(mysensor.read_angle())
    filt_angle.append(myfilter.applyFilter(raw_angle))
    sleep(1/1000.0)
plt.plot(t,raw_angle,'r')    
plt.plot(t,filt_angle,'k')
plt.show()
    