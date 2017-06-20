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
from sensors import *
from Adafruit_BNO055 import BNO055
import uh_utils as uh
import time, datetime, pytz
import os, inspect
import pandas as pd
import matplotlib.pyplot as plt
#==============================================================================
subjID = 'UH_IMUtest' # Data will be store in subj ID folder
filekey = ['IMU'] # list of file to record
expdataDir = 'Exp Data'

def get_timenow(key='%H:%M:%S'):
    '''
    %Y : YY; %m: mm; %d: dd
    %H : Hour; %M: Minute; %S: Seconds
    '''
    timenow = datetime.datetime.now(pytz.timezone('US/Central'))
    return timenow.strftime(key)
def print_stack():
    print('{}- Running: {}...'.format(get_timenow('%H:%M:%S'),
          inspect.stack()[1][3]),
          )      
#==============================================================================
def init():
    # Hardware setup
    rst_pin = 'P9_12'
    bno = BNO055.BNO055(rst = rst_pin)
    import Adafruit_GPIO.Platform as Platform
    import Adafruit_GPIO.I2C as I2C
    print('Default Bus:', I2C.get_default_bus())
    print(dir(bno._i2c_device))
    print('I2C address: {}'.format(bno._i2c_device._address))
    bus = bno._i2c_device._bus
    print('I2C bus: {}'.format(bus))
    print(dir(bus))
    print(bus._device)
    
#    import Adafruit_GPIO.I2C as I2C
#    print(I2C.get_default_bus())
    plat = Platform.platform_detect()
    print(dir(Platform))
    print('Platform: 2 for BBB: {}'.format(plat))
#    # Initialize the BNO055 and stop if something went wrong.
    if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
#    # Print system status and self test result.
#    status, self_test, error = bno.get_system_status()
#    print('System status: {0}'.format(status))
#    print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
#    # Print out an error if system status is in error mode.
#    if status == 0x01:
#        print('System error: {0}'.format(error))
#        print('See datasheet section 4.3.59 for the meaning.') 
#    # Print BNO055 software revision and other diagnostic data.
#    sw, bl, accel, mag, gyro = bno.get_revision()
#    print('Software version:   {0}'.format(sw))
#    print('Bootloader version: {0}'.format(bl))
#    # FileIO setup
#    myFile = uh.FileIO(subjID = subjID, logfilekey = filekey)
#    myFile.make_expfiles()
#    txtheader = 'Time Acc_x Acc_y Acc_z Heading Roll Pitch \n'
#    myFile.logfile['IMU'].write(txtheader)
#    timer = time
#    return bno, myFile, timer
    
#==============================================================================
def streamData(**kwargs):
    print_stack()
    # Parsers
    opt = {'verbose':False,
           'gc': False}        
    if kwargs: # if no input is given
        opt.update((key, kwargs[key])
                            for key in ('verbose','gc')
                            if key in kwargs
                            )
    print('Input Args: {}'.format(opt))
    bno, myFile, timer = init()
    start = timer.time()
    count = 0
    print 'START: IMU data collection!'
    try:
        while(1):
            timelog = timer.time() - start
            accx, accy, accz = bno.read_linear_acceleration()
            
            heading, roll, pitch = bno.read_euler()
            myFile.logfile['IMU'].write('%.2f %.2f %.2f %.2f %.2f %.2f %.2f \n' \
                                        %(timelog,accx, accy, accz,\
                                          heading,roll,pitch))
            if opt['verbose'] is True:
                if count%100 ==  0:
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
    plt.plot(pddf['Time'], pddf['Acc_z'],'r')
    plt.plot(pddf['Time'], pddf['Roll'])
    plt.legend(['Acc_z', 'Roll'])
    plt.show()
    return 1

#==============================================================================
def main():
    init()
#    streamData()
#    plot() 
    
#==============================================================================
if __name__ == '__main__':
    main()