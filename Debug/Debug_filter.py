# -*- coding: utf-8 -*-
"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Wed May 24 15:26:15 2017
"""
#==============================================================================
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import numpy as np
import uh_utils as uh
import matplotlib.pyplot as plt
#==============================================================================
Fs = 100
t = np.arange(0,5,1.0/Fs)
actual_signal = [10*np.cos(6*2*(np.pi)*ti) for ti in t]
noise = [5*np.cos(40*2*(np.pi)*ti) for ti in t]
rawSig = np.add(actual_signal,noise)
myfilter = uh.uh_filter(2,[0.1,7],100,'bandpass')
filtSig = np.zeros((np.size(rawSig),1))
for i in range(0,np.size(rawSig)):    
    filtSig[i] = myfilter.applyFilter(rawSig[i])
#==============================================================================
# Plot
plt.plot(t,rawSig,'b')
plt.plot(t,actual_signal,'r',linewidth = 1.5)
plt.plot(t,filtSig,'k--')
plt.show()