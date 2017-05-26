"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sun May 14 06:13:42 2017
"""
# Description: Sensors modules interacts with all sensors that connected
# to BBB board.
#==============================================================================
# START CODE
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
from bbio import * # Use pyBBIO library.
from uh_utils import AttrDisplay # In uh_classtools.py file
from time import sleep
#==============================================================================
# sensor is a parent class
class sensor(AttrDisplay):
    def __init__(self, name, sensortype,inputPIN):
        self.name = name
        self.type = sensortype
        self.inputPIN = inputPIN
        self.eventEnable = 0
    def sensor_Callback(self,channel):
        print self.name + ": event Callback"
#==============================================================================
# Digital Sensor
#==============================================================================
class digitalSensor(sensor):
    def __init__(self,name,inputPIN):
        sensor.__init__(self,name,'Digital',inputPIN) #Init by parent class
        self.setup()        
    def setup(self):
#        GPIO.setup(self.inputPIN, GPIO.IN)
        pinMode(self.inputPIN, INPUT)
        if not self.eventEnable:
            self.addEvent()
    # Add event. When event happens, callback function is called.
    def addEvent(self):
#        GPIO.add_event_detect(self.inputPIN,GPIO.RISING, 
#                              callback = self.sensor_Callback,bouncetime = 200)
        attachInterrupt(self.inputPIN, callback = self.sensor_Callback, edge = BOTH)
        self.eventEnable = 1    
    def read(self):
#        GPIO.setup(self.inputPIN, GPIO.IN)
#        return GPIO.input(self.inputPIN)'
        pinMode(self.inputPIN, INPUT)
        return digitalRead(self.inputPIN)
#==============================================================================
class limitSwitch(digitalSensor):
    def __init__(self,name,inputPIN):
        digitalSensor.__init__(self,name,inputPIN)
    def sensor_Callback(self,channel):
        print self.name + "is Activated. CallbackFcn is called"
#==============================================================================
# Analog sensors
#==============================================================================
class analogSensor(sensor):
    def __init__(self,name,inputPIN):
        sensor.__init__(self,name,'Analog',inputPIN) #Init by parent class
        self.setup()        
    def setup(self):
#        ADC.setup()
        pass
    def read(self):        
#        return ADC.read(self.inputPIN)        
        return analogRead(self.inputPIN)
#==============================================================================
# Sensors that use SPI interface
#==============================================================================
class SPIsensor():
    def __init__(self, csPin, clkPin, dataPin, nBits, sigRange):
        '''
        dataPin: SPI input Pin on BBB
        clkPin : SPI_SCLK Pin on BBB, clock pin
        csPin : SPI_CS pin on BBB, chip select pin in SPI interface
        nBits: number of bits from sensor, define its resolution.
        sigRange: Range of the actual signal that we want to measure, e.g., 360 deg
        '''
        # Define PIN IO
        self.csPin = csPin
        self.clkPin = clkPin
        self.dataPin = dataPin
        self.nBits = nBits
        self.sigRange = sigRange
        GPIO.setup(self.csPin,GPIO.OUT)
        GPIO.setup(self.clkPin,GPIO.OUT)
        GPIO.setup(self.dataPin,GPIO.IN)
#        pinMode(self.csPin,OUTPUT)        
#        pinMode(self.clkPin,OUTPUT)
#        pinMode(self.dataPin,INPUT) # Set dataPin as INPUT using pinMode func in bbio
        # Compute sensor resolution
        self.res = float(self.sigRange)/(2**self.nBits)
    def read(self):
        # This follow SPI interface serial communication.        
        GPIO.output(self.csPin, GPIO.HIGH)
        GPIO.output(self.clkPin, GPIO.HIGH)
        sleep(1/1000000.0)
        GPIO.output(self.csPin, GPIO.LOW)
        GPIO.output(self.clkPin, GPIO.LOW)
        sleep(1/1000000.0)
        raw_value = 0
        inputstream = 0    
        for i in range(16):
            GPIO.output(self.clkPin, GPIO.HIGH)
            sleep(1/1000000.0)
            inputstream = GPIO.input(self.dataPin)
            raw_value = raw_value*2 + inputstream
            GPIO.output(self.clkPin, GPIO.LOW)
            sleep(1/1000000.0)
        return raw_value
#==============================================================================
class SPIencoder(SPIsensor):
    def __init__(self,csPin, clkPin, dataPin,nBits):
        SPIsensor.__init__(self,csPin, clkPin, dataPin,nBits,360) #Init by parent class
    def read_angle(self):
        rawvalue = self.read()
        return rawvalue/2**(16-self.nBits)*self.res
#        print rawvalue
#        angle = rawvalue # Right shift to 8 bits and times res        
#        return angle
        
    
        
                

