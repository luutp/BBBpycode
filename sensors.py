"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sun May 14 06:13:42 2017
"""
# Description: Sensors modules interacts with all sensors that connected
# to BBB board.
# Abstract class
#==============================================================================
# START CODE
#from abc import ABCMeta, abstractmethod # Package to create abstrat class
import Adafruit_BBIO.GPIO as GPIO
from time import sleep
from uh_classtools import AttrDisplay # In uh_classtools.py file
class sensor(AttrDisplay):
    # sensor is a parent class
    def __init__(self, name, sensortype,inputPIN):
        self.name = name
        self.type = sensortype
        self.inputPIN = inputPIN
        self.eventEnable = 0
    def sensor_Callback(self,channel):
        print self.name + " is HIGH"
# Digital Sensor class to handle digital input        
class digitalSensor(sensor):
    def __init__(self,name,inputPIN):
        sensor.__init__(self,name,'Digital',inputPIN) #Init by parent class
        self.setup()        
    def setup(self):
        GPIO.setup(self.inputPIN, GPIO.IN)
        if not self.eventEnable:
            self.addEvent()
    # Add event. When event happens, callback function is called.
    def addEvent(self):
        GPIO.add_event_detect(self.inputPIN,GPIO.RISING, 
                              callback = self.sensor_Callback,bouncetime = 200)
        self.eventEnable = 1    
    def read(self):
        GPIO.setup(self.inputPIN, GPIO.IN)
        return GPIO.input(self.inputPIN)
    

class limitSwitch(digitalSensor):
    def __init__(self,name,inputPIN):
        digitalSensor.__init__(self,name,inputPIN)
    def sensor_Callback(self,channel):
        print self.name + "is Activated. CallbackFcn is called"
        


        
        




