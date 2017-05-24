"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sun May 14 02:46:53 2017
"""
# Description:
#==============================================================================
# START CODE
import os
import shutil
import uh_utils as uh
import gvar_def
from time import sleep
import math
import matplotlib.pyplot as plt
import numpy.matlib as np
from scipy.signal import butter, tf2ss, lfilter, filtfilt
from sensors import *
gvar = gvar_def.gvar()

# BBB GPIO
#import Adafruit_BBIO.GPIO as GPIO
# Blink LED
#digOutPin = 'P9_23'
#GPIO.setup(digOutPin, GPIO.OUT)
#for i in range(0,3):
#    GPIO.output(digOutPin, GPIO.HIGH)
#    sleep(0.5)
#    GPIO.output(digOutPin, GPIO.LOW)    
#    sleep(0.5)

# Digital Input, 1kOhm register pull down
#digInPin = 'P9_27'    
#GPIO.setup(digInPin, GPIO.IN)
#count = 0
#while(1):
#    print "count: %d" %count
#    count = count + 1
#    if GPIO.input(digInPin):
#        print "Button Pressed"            
#    if count == 10:
#        break
#    sleep(1)

# Digital input to turn on LED
#digInPin = 'P9_30'  
#digInPinBreak = 'P9_27'    
#digOutPin = 'P9_23'
#GPIO.setup(digInPin, GPIO.IN)
#GPIO.setup(digInPinBreak, GPIO.IN)
#GPIO.setup(digOutPin, GPIO.OUT)
#while(1):
#    if GPIO.input(digInPinBreak):
#        print "STOP"
#        break
#    if GPIO.input(digInPin):
#        print "Button Pressed"            
#        GPIO.output(digOutPin, GPIO.HIGH) 
#    else:
#        GPIO.output(digOutPin, GPIO.LOW) 
#    sleep(0.1)
#GPIO.cleanup()
#

#sdcard = uh.sdcard(gvar.sdcardLabel)
#uh.list_dirtree(sdcard.path)
#
##Test File IO
##print uh.get_today()
#myFileIO = uh.FileIO(gvar.expDataDirName,'UH_AB_01',['eeg'])
#logfiles = myFileIO.make_expfiles()
#uh.list_dirtree(myFileIO.expDataDirPath)

#sdcard = uh.sdcard('BBB_SDCARD')
#print sdcard.path
#print os.listdir(sdcard.expDataDirPath)
##print myFileIO.expDataDirPath
#print sdcard.expDataDirPath
#sdcard.cleanup()
#sdcard.make_expDataDir()
#sdcard.save_expdata(myFileIO.expDataDirPath,sdcard.expDataDirPath)
#for root,dirs,files in os.walk(sdcard.expDataDirPath):
#    print root
#    print dirs
#    print files

#print os.listdir(sdcard.path)
#sdcard = os.path.join('/media','BBB_SDCARD')
#print os.listdir(sdcard)
#print os.path.abspath('/media/BBB_SDCARD')
#print os.listdir(os.path.join(os.path.abspath(os.),'BBB_SDCARD'))
#print os.path.pardir

#from uh_genexpfiles import *
#from uh_utils import *
#import uh_utils as uh
#myfileio = uh.FileIO('Exp Data','UH_AB_01',['eeg'])
#mytime = uh.timenow()
#print uh.timenow().tday
#print myfileio.subjdir



#logfile = uh_genexpfiles()
#logfile['eeg'].write("Hello, this is EEG file")
#print logfile['eeg'].name
#import numpy.matlib as np
#from scipy.signal import butter
#import matplotlib.pyplot as plt
#x = np.linspace(0,10,20)
#y = np.power(x,2)
#plt.plot(x,y)
#plt.show()
#print "DONE"

#a = np.array([1,2,3])
##b = np.array([4,5,6])
#unitmat = 2*np.eye(3);
#print np.size(unitmat,1)
#print gvar.bbbPIN
#mysensor = digitalSensor("Limit Switch", "P9_27")
#print gvar.bbbPin
#mysensor = limitSwitch("Limit Switch", gvar.bbbPin["SwitchFW"])
#mypot = analogSensor("Potentionmeter","P9_36")
#while (1):    
#    sleep(0.5)
#    print mypot.read()
#    if mysensor.read():
#        print "STOP"
#        break
#GPIO.cleanup()        

#mygvar = gvar
#print mygvar.bbbPinmapfilename
#mygvar.bbbPinDef()
#print mygvar.bbbPin

#num,den =  uh.highpass(4,6,100)
#passband = [0.75*2/30, 5.0*2/30]
#b, a = butter(4,6 / (100*0.5), 'high')
#print b 
#print a
#print butter(5,[3/50, 6/50],'bandpass')
#print ['%.4f' % i for i in num]
#print ['%.4f' % i for i in den]
#num, den = uh.highpass(4,6,100)
#print num, den
#print num
#print den
#print tf2ss(num,den)
#print tf2ss(den,num)
#print A
#print B
#print C
#print D
#==============================================================================
# 
#==============================================================================
#Fs = 100
#t = np.arange(0,5,1.0/Fs)
#actual_signal = [10*np.cos(6*2*(np.pi)*ti) for ti in t]
#noise = [5*np.cos(40*2*(np.pi)*ti) for ti in t]
#rawSig = np.add(actual_signal,noise)
#myfilter = uh.uh_filter(2,[0.1,7],100,'bandpass')
#filtSig = np.zeros((np.size(rawSig),1))
#for i in range(0,np.size(rawSig)):    
##    print myfilter.Xnn
#    filtSig[i] = myfilter.applyFilter(rawSig[i])
##num,den = butter(2, 7/(100*0.5), 'low')
##[A,B,C,D] = tf2ss(num,den)
##Xnn = np.zeros((np.size(A,1),1))
##filtSig = np.zeros((np.size(rawSig),1))
##for i in range(0,np.size(rawSig)):    
##    u = rawSig[i]
##    myXnn = Xnn
##    Xn = np.add(np.matmul(A,myXnn), B*u)
##    ytemp = np.add(np.matmul(C,myXnn), D*u)
##    filtSig[i] = ytemp
##    Xnn = Xn
##filtered_signal = lfilter(num,den,rawSig)
#plt.plot(t,rawSig,'b')
#plt.plot(t,actual_signal,'r',linewidth = 1.5)
#plt.plot(t,filtSig,'k--')
##plt.plot(t,filtered_signal,'g--')
#plt.show()

# Test encoder
# Set variables for the pins connected to the ADC:
data_pin = GPIO1_15  # P8.15
clk_pin  = GPIO1_14  # P8.16
cs_pin   = GPIO0_27  # P8.17
myencoder = SPIencoder(data_pin, clk_pin, cs_pin,10)
print myencoder.readEncoder()