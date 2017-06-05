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
import uh_utils as uh
from FSI_control import cirBuffer
#==============================================================================
kinfile = sio.loadmat('Python_acc.mat')
accarr = kinfile['acc']
acc = accarr.tolist()
kinfile = sio.loadmat('Python_footOrientation.mat');
temp = kinfile['footOrientation']                     
footOrientation = temp.tolist()
fs = 30
accbuff = cirBuffer(3)
oribuff = cirBuffer(3)
myfilter1 = uh.uh_filter(2,[0.1],30,'high')
myfilter2 = uh.uh_filter(2,[0.1],30,'high')
HCcatching = False
TOcatching = False
thres = -4
plt.close()
myfig = plt.figure()
myax = plt.gca()
for i in xrange(2000):
    accbuff.append(myfilter1.applyFilter(acc[i]))
    oribuff.append(myfilter2.applyFilter(footOrientation[i]))
    if not None in accbuff.data:
        pass
#        print ['%.2f' %item for item in accbuff.data]
#        print '%.2f' %accbuff.mean
    if not HCcatching:
        if accbuff.mean < thres:
            if accbuff.isDescend():
                print 'Waiting for HC'
                HCcatching = True
    else:
        if not accbuff.isDescend():
            print 'Detected: HC'
            hcplt = plt.axvline(i,color='r',linestyle = ':')
            HCcatching = False
    # Detect Toe-off
    if not TOcatching:
        if oribuff.mean < -5:
            if oribuff.isDescend():
                print 'Waiting for TO'
                TOcatching = True
    else:
        if not oribuff.isDescend():
            print 'Detected: TO'
            toplt = plt.axvline(i,color='g',linestyle = ':')
            TOcatching = False

filtacc = myfilter1.applyFilter(acc)
filtfootOrientation = myfilter2.applyFilter(footOrientation)
accplot, = plt.plot(filtacc,'b')
footOriplot, = plt.plot(filtfootOrientation,'k')
plt.ylabel('Foot Acc and Orientation')
plt.xlabel('Samples')
plt.legend([accplot,footOriplot,hcplt,toplt],['Raw Acc_z','Foot Orientation','Heel Contact','Toe Off'],loc='upper right')

