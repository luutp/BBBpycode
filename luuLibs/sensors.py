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
class sensors(object,utils.parentClass):
    '''
    This is an abstract class which cannot be instantiate
    '''
    __metaclass__ = ABCMeta
    def __init__(self): pass
    @property
    def name(self):
        return 'sensorName'
    @property
    def sensorType(self):
        return 'Digitial/Analog'
    @abstractmethod
    def setup(self): pass
    @abstractmethod
    def readData(self): pass
#==============================================================================
class digSensor(sensors):
    def __init__(self,**kwargs):
        varargin = utils.get_varargin({'name':'digSensor',
                                 'sensorType': 'Digital',
                                 'pin': 'Px_xx'},kwargs)
        for key,val in varargin.items():
            # Attributes in sensor abstract class are static
            setattr(self,'_{}'.format(key),val)
    @property #Override this property
    def name(self): return self._name
    @property
    def sensorType(self): return self._sensorType
    @property
    def pin(self): return self._pin
                  
    def setup(self): pass
    def readData(self): pass
#==============================================================================
def main():
    mysensor = digSensor()
    mysensor.print_Me()

#==============================================================================
if __name__ == '__main__':
    main()
