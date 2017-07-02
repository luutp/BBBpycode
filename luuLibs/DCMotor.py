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
 
 .. figure:: icons/logo_uh.jpg
    :width: 280px
    :height: 80px
    :align: left
    
    **Department of Electrical & Computer Engineering**
    
    **Laboratory for Noninvasive Brain-Machine Interface Systems**
    
    `Facebook Page <https://www.facebook.com/UHBMIST/>`_
    
 Created on: *Sun Jul 02 01:19:20 2017*
 
 Python version: *2.7*
"""
#==============================================================================
# Import packages
import utils
#==============================================================================
# DEFINE
#==============================================================================
class DCMotor(object,utils.parentClass):
    def __init__(self, **kwargs):
        # Parsers
        varargin = utils.get_varargin({'brand': 'Maxon',
                                 'tag': 'EC305013'},
                                kwargs)
        for key, val in varargin.items():
            setattr(self,key,val)
        self.get_specs()
            
    @property
    def name(self):
        return '{}_{}'.format(self.brand,self.tag)
    
    def get_specs(self):
        motorspecs = eval('{}()'.format(self.name))
        for key,val in motorspecs.items():
            setattr(self,key,val)
    
#==============================================================================
def Maxon_EC305013():
    '''
    Maxon EC motor EC 305013.
    
    `Datasheet <http://www.maxonmotorusa.com/maxon/view/product/motor/ecmotor/ec4pole/305013>`_
    '''
    motor = {'type': 'EC', # Part number
            'power':200, # Watt
            'normVolt': 24, # Volt
            'normSpeed': 16100, # rmp
            'normTorque': 94.6, # mNm
            'normAmp': 7.58, # Amp
            'constTorque': 13.6, # mNm/A
            'constSpeed': 700, # rmp/V
            }
    return motor
    
#==============================================================================
def main():
    m1 = DCMotor()
    m1.print_Me()

#==============================================================================
if __name__ == '__main__':
    main()
