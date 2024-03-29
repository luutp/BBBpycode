"""
 Description:
     
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Mon Jun  5 00:58:46 2017
"""
#==============================================================================
# START CODE
# Hardware setup. BNO055 connection to BBB.
# Vin to 3.3 V on BBB
# GND to GND on BBB
# SDA to P9_20 on BBB, I2C2_SDA
# SCL to P9_19 on BBB, I2C2_SCL
# RST: Reset pin to P9_12 on BBB
# Pinout Ref: https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/pinouts
#from sensors import *
from Adafruit_BNO055 import BNO055
import uh_utils as uh
import time, datetime, pytz
import os, inspect
import pandas as pd
import matplotlib.pyplot as plt
import Adafruit_GPIO.I2C as I2C
from FSI_control import cirBuffer

#==============================================================================
subjID = 'UH_IMUtest' # Data will be store in subj ID folder
filekey = ['IMU'] # list of file to record
expdataDir = 'Exp Data'
PLATFORM = ['BBB', 'BBB_WIFI'] # BBB or BBB_WIFI. option to set I2C bus.
#==============================================================================
def get_timenow(key='%H:%M:%S'):
    '''
    %Y : YY; %m: mm; %d: dd
    %H : Hour; %M: Minute; %S: Seconds
    '''
    timenow = datetime.datetime.now(pytz.timezone('US/Central'))
    return timenow.strftime(key)
    
#==============================================================================
def print_stack():
    print('{}- Running: {}...'.format(get_timenow('%H:%M:%S'),
          inspect.stack()[1][3]),
          )      
          
#==============================================================================
def get_platform():
    # Check if device is BBB or BBB Wifi with Wlan feature
    bbb = PLATFORM[0] # Default as BeagleBone black
    wifiInfo = '/proc/net/wireless'
    fid = open(wifiInfo)
    for line in fid:
        if 'wlan0' in line:
            bbb = PLATFORM[1]
    print('Device: {}'.format(bbb))
    fid.close()
    return bbb
    
#==============================================================================
def init():
    # Setup I2C connection with BNO055
    rst_pin = 'P9_12'
    device = get_platform()
    if device == PLATFORM[0]: # BBB
        bno = BNO055.BNO055(rst = rst_pin) # I2C2 bus number is 1
    elif device == PLATFORM[1]: #BBB_WIFI
    # Modify BNO055.py from Adafruit by adding kw argument busnum = None
        bno = BNO055.BNO055(rst = rst_pin, busnum = 2) # I2C2 bus number is 2
    # Initialize the BNO055 and stop if something went wrong.
    if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
    # Print system status and self test result.
    status, self_test, error = bno.get_system_status()
    print('System status: {0}'.format(status))
    print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
    # Print out an error if system status is in error mode.
    if status == 0x01:
        print('System error: {0}'.format(error))
        print('See datasheet section 4.3.59 for the meaning.') 
    # Print BNO055 software revision and other diagnostic data.
    sw, bl, accel, mag, gyro = bno.get_revision()
    print('Software version:   {0}'.format(sw))
    print('Bootloader version: {0}'.format(bl))
    # FileIO setup
    myFile = uh.FileIO(subjID = subjID, logfilekey = filekey)
    myFile.make_expfiles()
    txtheader = 'Time Acc_x Acc_y Acc_z Heading Roll Pitch gaitEvent\n'
    myFile.logfile['IMU'].write(txtheader)
    timer = time
    return bno, myFile, timer
    
#==============================================================================
def streamData(**kwargs):
    print_stack()
    # Parsers
    varargin = {'verbose':False,
           'gc': False}        
    if kwargs: # if no input is given
        varargin.update((key, kwargs[key])
                            for key in ('verbose','gc')
                            if key in kwargs
                            )
    print('Input Args: {}'.format(varargin))
    bno, myFile, timer = init()
    start = timer.time()
    count = 0
    print 'START: IMU data collection!'
    try:        
        if varargin['gc'] is False:
            while(1):
                timelog = timer.time() - start
                accx, accy, accz = bno.read_linear_acceleration()
                heading, roll, pitch = bno.read_euler()
                myFile.logfile['IMU'].write('%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f\n' \
                                            %(timelog,accx, accy, accz,\
                                              heading,roll,pitch,\
                                              0))
                if varargin['verbose'] is True:
                    if count % 100 ==  0:
                        print('{}- Streaming IMU- Head: {}; Roll: {}; Pitch: {}...'.format(float("{0:.2f}".format(timelog)),
                              int(heading), int(roll), int(pitch)))
                    count+=1
        else:
            fs = 100
            accbuff = cirBuffer(3)
            oribuff = cirBuffer(3)
            myfilter1 = uh.uh_filter(2,[0.1],fs,'high')
            myfilter2 = uh.uh_filter(2,[0.1],fs,'high')
            HCcatching = False
            TOcatching = False
            lastEvent = 4
            while(1):
                timelog = timer.time() - start
                accx, accy, accz = bno.read_linear_acceleration()
                heading, roll, pitch = bno.read_euler()
                accbuff.append(myfilter1.applyFilter(accz))
                oribuff.append(myfilter2.applyFilter(roll))
                gcEvent = 0
                if not HCcatching:
                    if oribuff.mean > 10:
                        if oribuff.isAscend():
                            HCcatching = True
                else:
                    if oribuff.isDescend():
                        if lastEvent == 4:
                            print 'Detected: HC'
                            gcEvent = 1
                            lastEvent = 1
                        HCcatching = False
                # Detect Toe-off
                if not TOcatching:
                    if oribuff.mean < -15:
                        if oribuff.isDescend():
                            TOcatching = True
                else:
                    if oribuff.isAscend():
                        if lastEvent == 1:
                            print 'Detected: TO'
                            gcEvent = 4
                            lastEvent = 4
                        TOcatching = False
                myFile.logfile['IMU'].write('%.2f %.2f %.2f %.2f %.2f %.2f %.2f %d\n'\
                                            %(timelog,accx, accy, accz,\
                                              heading,roll,pitch,\
                                              gcEvent))
                if varargin['verbose'] is True:
                    if count % 100 ==  0:
                        print('{}- Streaming IMU- Head: {}; Roll: {}; Pitch: {}...'.format(float("{0:.2f}".format(timelog)),
                              int(heading), int(roll), int(pitch)))
                    count+=1
    except KeyboardInterrupt:
        myFile.logfile['IMU'].close()
        print 'EXIT: Data collection completed!'
#        
#==============================================================================
def get_pydir():
    pyFileDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return pyFileDir
    
#==============================================================================
def get_datadir():
    pycodeDir = get_pydir()
    luuDir = os.path.dirname(pycodeDir)
    dataDir = os.path.join(luuDir, expdataDir, subjID)
    return dataDir
    
#==============================================================================
def list_files():
    startpath = os.path.dirname(get_datadir())
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

#==============================================================================
def del_files(**kwargs):
    # Get the most current data file or input filename
    if os.path.isdir(get_datadir()):
        filelist = os.listdir(get_datadir())
        filelist = sorted(filelist)
    else:
        print('{} data folder is not exist'.format(get_datadir().split('/')[-1]))
        return 0
    if not kwargs:
        filename = filelist
    else:
        for key, val in kwargs.items():
            if key.lower() == 'trial':
                filename = filelist[val]
            if key.lower() == 'filename':
                filename = val
    for f in filename:
        os.remove(os.path.join(get_datadir(),f))
        
#==============================================================================
def psudo_gc(**kwargs):
        # Get the most current data file or input filename
    if os.path.isdir(get_datadir()):
        filelist = os.listdir(get_datadir())
        filelist = sorted(filelist)
    else:
        print('{} data folder is not exist'.format(get_datadir().split('/')[-1]))
        return 0
    if not kwargs:
        filename = filelist[-1]
    else:
        for key, val in kwargs.items():
            if key.lower() == 'trial':
                filename = filelist[val]
            if key.lower() == 'filename':
                filename = val
    print('Filename: {}'.format(filename))
    fullfilename = os.path.join(get_datadir(),filename)
    pddf = pd.read_csv(fullfilename,sep = " ", header = 0)
    
    acczLog = pddf['Acc_z']
    rollLog = pddf['Roll']
    timeLog = pddf['Time']
    fs = 100
    accbuff = cirBuffer(3)
    oribuff = cirBuffer(3)
    myfilter1 = uh.uh_filter(2,[0.1],fs,'high')
    myfilter2 = uh.uh_filter(2,[0.1],fs,'high')
    HCcatching = False
    TOcatching = False
    gcEventList = []
    lastEvent = 4
    for idx, t in enumerate(timeLog):
        accz = acczLog[idx]
        roll = rollLog[idx]
        accbuff.append(myfilter1.applyFilter(accz))
        oribuff.append(myfilter2.applyFilter(roll))
        gcEvent = 0
        if not HCcatching:
            if oribuff.mean > 10:
                if oribuff.isAscend():
                    HCcatching = True
        else:
            if oribuff.isDescend():
                if lastEvent == 4:
                    print 'Detected: HC'
                    gcEvent = 1
                    lastEvent = 1
                HCcatching = False
        # Detect Toe-off
        if not TOcatching:
            if oribuff.mean < -15:
                if oribuff.isDescend():
                    TOcatching = True
        else:
            if oribuff.isAscend():
                if lastEvent == 1:
                    print 'Detected: TO'
                    gcEvent = 4
                    lastEvent = 4
                TOcatching = False
        gcEventList.append(gcEvent)
    plt.plot(timeLog, acczLog,'b')
    plt.plot(timeLog, rollLog,'g')
    plt.legend(['Acc_z', 'Roll'])
    for idx, gc in enumerate(gcEventList):
        if gc == 1:
            plt.axvline(timeLog[idx],color='r',linewidth = 1.5)
        elif gc ==4:
            plt.axvline(timeLog[idx],color='k',linewidth = 0.75)
    plt.show()
                
#==============================================================================
def plot(**kwargs):
    '''
    Plot the most updated data if no input argument
    
    Optional input arguments:
        
        'trial' = 
        
        'filename' = 
    '''
    # Get the most current data file or input filename
    if os.path.isdir(get_datadir()):
        filelist = os.listdir(get_datadir())
        filelist = sorted(filelist)
    else:
        print('{} data folder is not exist'.format(get_datadir().split('/')[-1]))
        return 0
    if not kwargs:
        filename = filelist[-1]
    else:
        for key, val in kwargs.items():
            if key.lower() == 'trial':
                filename = filelist[val]
            if key.lower() == 'filename':
                filename = val
    print('Filename: {}'.format(filename))
    fullfilename = os.path.join(get_datadir(),filename)
    pddf = pd.read_csv(fullfilename,sep = " ", header = 0)
    plt.plot(pddf['Time'], pddf['Acc_z'],'b')
    plt.plot(pddf['Time'], pddf['Roll'],'g')
    plt.legend(['Acc_z', 'Roll'])
    for idx, gc in enumerate(pddf['gaitEvent']):
        if gc == 1:
            plt.axvline(pddf['Time'][idx],color='r',linewidth = 1.5)
        elif gc ==4:
            plt.axvline(pddf['Time'][idx],color='k',linewidth = 0.75)
                
    plt.show()
    return 1
    
#==============================================================================
def read_txt(**kwargs):
    '''
    Plot the most updated data if no input argument
    
    Optional input arguments:
        
        'trial' = 
        
        'filename' = 
    '''
    # Get the most current data file or input filename
    if os.path.isdir(get_datadir()):
        filelist = os.listdir(get_datadir())
        filelist = sorted(filelist)
    else:
        print('{} data folder is not exist'.format(get_datadir().split('/')[-1]))
        return 0
    if not kwargs:
        filename = filelist[-1]
    else:
        for key, val in kwargs.items():
            if key.lower() == 'trial':
                filename = filelist[val]
            if key.lower() == 'filename':
                filename = val
    print('Filename: {}'.format(filename))
    fullfilename = os.path.join(get_datadir(),filename)
    fid = open(fullfilename)
    for line in fid:
        print(line)
    fid.close()
    
#==============================================================================
def main():
    init()
#    streamData(verbose=True, gc = True)
#    plot() 
#    psudo_gc()
    
#==============================================================================
if __name__ == '__main__':
    main()