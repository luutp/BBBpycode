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
from sensors import *
gvar = gvar_def.gvar()

# BBB GPIO
import Adafruit_BBIO.GPIO as GPIO
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
print gvar.bbbPIN
mysensor = digitalSensor("Limit Switch", "P9_27")
#mysensor = limitSwitch("Limit Switch", gvar.bbbPIN["SwitchFW"])
#while (1):    
#    sleep(0.5)
#    print "Running. Touch the switch to stop"
#    if mysensor.read():
#        print "STOP"
#        break
#GPIO.cleanup()        