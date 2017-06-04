# -*- coding: utf-8 -*-
"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sat Jun 03 21:04:10 2017
"""
#==============================================================================
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
#import uh_utils as uh
from FSI_control import *
#==============================================================================
kinfile = sio.loadmat('Python_acc.mat')
accarr = kinfile['acc']
acc = accarr.tolist()
fs = 30
plotbuff = cirBuffer(100)
fig = plt.figure()
ax = fig.add_subplot(111)

# some X and Y data
x = np.arange(10000)
y = np.random.randn(10000)

li, = ax.plot(x, y)

# draw and show it
ax.relim() 
ax.autoscale_view(True,True,True)
fig.canvas.draw()
plt.show(block=False)

# loop to update the data
while True:
    try:
        y[:-10] = y[10:]
        y[-10:] = np.random.randn(10)

        # set the new data
        li.set_ydata(y)

        fig.canvas.draw()

        sleep(0.01)
    except KeyboardInterrupt:
        break
#for i in xrange(1000):
#    plotbuff.append(acc[i])
#    if not None in plotbuff.data:
#        plt.plot(plotbuff.data)
#    plt.cla()
#    sleep(1/fs)
#plt.plot(plotbuff.data)    
#myfilter = uh.uh_filter(2,[0.1,6],30,'bandpass')
#filtSig = np.zeros((np.size(rawSig),1))
#for i in range(0,np.size(rawSig)):    
#    filtSig[i] = myfilter.applyFilter(rawSig[i])
#plt.figure()
#plt.plot(acc)
#plt.show()

