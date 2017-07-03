# -*- coding: utf-8 -*-
"""
Descriptions
#############
Function description

:param: input argument
:returns: output
:Example:

.. Note::
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.    

.. seealso::    

Authors
#######
 Trieu Phat Luu. *Email: tpluu2207@gmail.com*
 
 .. figure:: logo_uh.jpg
    :width: 280px
    :height: 80px
    :align: left
    
    **Department of Electrical & Computer Engineering**
    
    **Laboratory for Noninvasive Brain-Machine Interface Systems**
    
    `Facebook Page <https://www.facebook.com/UHBMIST/>`_
    
 Created on: *Sun Jul 02 02:22:32 2017*
 
 Python version: *2.7*
"""
#==============================================================================
# Import packages
import utils, mainBoard
from abc import ABCMeta, abstractmethod
#import Adafruit_BBIO.GPIO as GPIO
#import Adafruit_BBIO.ADC as ADC
#==============================================================================
# DEFINE
#==============================================================================
# Abstract Class sensors
#==============================================================================
class sensors(object,utils.parentClass):
    '''
    This is an abstract class which cannot be instantiate
    '''
    __metaclass__ = ABCMeta
    def __init__(self): pass
        
    @property
    def _SENSORTYPE(self):
        return {'DIG':'Digital', 
                'ANA':'Analog',
                'SPI':'SPI',
                'NAN':'Undefined'}
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,val = 'sensorName'):
        self._name = val
        
    @property
    def sensType(self):
        return self._sensType
    @sensType.setter
    def sensType(self,val):
        if not val or val not in self._SENSORTYPE.values():
            val = self._SENSORTYPE['NAN']
        self._sensType = val
    
    @property
    def resolution(self):
        return self._resolution
    @resolution.setter
    def resolution(self,val = None):
        self._resolution = val
    
    @property
    def rangevals(self):
        return self._rangevals
    @rangevals.setter
    def rangevals(self,val=None):
        self._rangevals = val
        
    @property
    def nBits(self):
        return self._nBits
    @nBits.setter
    def nBits(self,val=None):
        self._nBits = val
    
    @abstractmethod
    def setup(self): pass
    @abstractmethod
    def readData(self): pass
    
    def threshold(self,val):        
        if self.rangevals is not None:
            if val < self.rangevals[0]:
                val = self.rangevals[0]
            elif val > self.rangevals[1]:
                val = self.rangevals[1]
        return val

#==============================================================================
# DIGITAL SENSOR
#==============================================================================
class digitalSens(sensors):
    '''
    Digital sensors
    '''
    def __init__(self,**kwargs):
        varargin = utils.get_varargin({'name':'digSensor',
                                 'sensType': 'Digital',
                                 'pin': 'Px_xx'},kwargs)
        for key,val in varargin.items():
            # Attributes in sensor abstract class are static
            setattr(self,'{}'.format(key),val)
        self.setup()
    #==============================================================================
    def setup(self):
        mainBoard.set_GPIO(self.pin,'IN')
        
    def readData(self):
        mainBoard.get_DI(self.pin)
        
#==============================================================================
# Analog sensors
#==============================================================================
class analogSens(sensors):
    '''
    Analog sensor
    '''
    def __init__(self,**kwargs):
        varargin = utils.get_varargin({'name':'Analog Sensor',
                                 'sensType': 'Analog',
                                 'pin': 'Px_xx'},kwargs)
        for key,val in varargin.items():
            # Attributes in sensor abstract class are static
            setattr(self,'{}'.format(key),val)
        self.setup()
    #==============================================================================
    def setup(self):
        mainBoard.setup_ADC()
        
    def readData(self):        
        mainBoard.get_ADC(self.pin)
#==============================================================================
# Sensors that use SPI interface
#==============================================================================
class SPIsensor(sensors):
    def __init__(self, csPin, clkPin, dataPin, nBits, sigRange):
        '''
        Inputs:
        #######
         :dataPin: SPI input Pin on BBB
         :clkPin: SPI_SCLK Pin on BBB, clock pin
         :csPin: SPI_CS pin on BBB, chip select pin in SPI interface
         :nBits: number of bits from sensor, define its resolution.
         :sigRange: Range of the actual signal that we want to measure, e.g., 360 deg
        '''
        # Define PIN IO
        self.csPin = csPin
        self.clkPin = clkPin
        self.dataPin = dataPin
        self.nBits = nBits
        self.sigRange = sigRange
#        
#        GPIO.setup(self.csPin,GPIO.OUT)
#        GPIO.setup(self.clkPin,GPIO.OUT)
#        GPIO.setup(self.dataPin,GPIO.IN)
#        # Compute sensor resolution
#        self.res = float(self.sigRange)/(2**self.nBits)
#    def readData(self):
#        # This follow SPI interface serial communication.        
#        GPIO.output(self.csPin, GPIO.HIGH)
#        GPIO.output(self.clkPin, GPIO.HIGH)
#        sleep(1/1000000.0)
#        GPIO.output(self.csPin, GPIO.LOW)
#        GPIO.output(self.clkPin, GPIO.LOW)
#        sleep(1/1000000.0)
#        raw_value = 0
#        inputstream = 0    
#        for i in range(16):
#            GPIO.output(self.clkPin, GPIO.HIGH)
#            sleep(1/1000000.0)
#            inputstream = GPIO.input(self.dataPin)
#            raw_value = raw_value*2 + inputstream
#            GPIO.output(self.clkPin, GPIO.LOW)
#            sleep(1/1000000.0)
#        return raw_value
        
#==============================================================================
def main():
    ana = analogSens()
    dig = digitalSens()
    print(ana.sensType)
    print(dig.sensType)
    ana.nBits = 12
    print(ana.__dict__)
#    mysensor._rangevals = [-1,1]
#    print('threshold val: {}'.format(mysensor.threshold(2)))
#    print(dir(mysensor))
#    mysensor.nBits = 12
#    print(mysensor.resolution)
#    mysensor.print_Me()

#==============================================================================
if __name__ == '__main__':
    main()
