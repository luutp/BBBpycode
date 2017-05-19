"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sun May 14 06:13:42 2017
"""
# Description: Sensors modules interacts with all sensors that connected
# to BBB board.
# Classes: 
#   limit_switch
#   strain_gauge
#   encoder
#   IMU
#==============================================================================
# START CODE
from abc import ABCMeta, abstractmethod # Package to create abstrat class
import Adafruit_BBIO.GPIO as GPIO
from time import sleep
# Interface or abstract class
class sensor():
    # Sensor Abtract class
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_name(self): pass
    @abstractmethod
    def get_type(self): pass

class digitalSensor(sensor):
    def __init__(self,name,inputPIN):
        self.name = name
        self.type = 'Digital'
        self.inputPIN = inputPIN
        super(digitalSensor,self).__init__()
    def get_name(self):
        return self.name
    def get_type(self):
        return self.type
    def get_pin(self):
        return self.inputPIN
    def read(self):
        GPIO.setup(self.inputPIN, GPIO.IN)
        return GPIO.input(self.inputPIN)
        
mysensor = digitalSensor("Limit Switch", "P9_27")
print mysensor.get_pin()
while (1):    
    sleep(0.5)
    print "Running. Touch the switch to stop"
    if mysensor.read():
        print "STOP"
        break
        
        




