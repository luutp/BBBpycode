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
        ADC.setup()
    def read(self):        
        return ADC.read(self.inputPIN)        
#==============================================================================
# Sensors that use SPI interface
#==============================================================================
class SPIsensor(sensor):
    def __init__(self, dataPin, clkPin, csPin, nBits, sigRange):
        '''
        dataPin: SPI input Pin on BBB
        clkPin : SPI_SCLK Pin on BBB, clock pin
        csPin : SPI_CS pin on BBB, chip select pin in SPI interface
        nBits: number of bits from sensor, define its resolution.
        sigRange: Range of the actual signal that we want to measure, e.g., 360 deg
        '''
        # Define PIN IO
        self.dataPin = dataPin
        self.clkPin = clkPin
        self.csPin = csPin
        self.nBits = nBits
        self.sigRange = sigRange
        pinMode(self.dataPin,INPUT) # Set dataPin as INPUT using pinMode func in bbio
        pinMode(self.clkPin,OUTPUT)
        pinMode(self.csPin,OUTPUT)        
        # Compute sensor resolution
        self.res = float(self.sigRange)/(2**self.nBits)
    def read(self):
        # This follow SPI interface serial communication.        
        digitalWrite(self.clkPin, LOW)
        digitalWrite(self.csPin, LOW)
        for i in range(17):
            digitalWrite(self.clkPin, HIGH)
            delay(10)
            inputstream = digitalRead(self.dataPin)
            raw_value = ((raw_value << 1) + inputstream);
            digitalWrite(_clock, LOW);
        return raw_value
#==============================================================================
class SPIencoder(SPIsensor):
    def __init__(self,dataPin,clkPin,csPin,nBits):
        SPIsensor.__init__(self,dataPin,clkPin,csPin,nBits,360) #Init by parent class
    def readEncoder(self):
        rawvalue = self.read()
        angle = rawvalue>>(18-self.nBits) * self.res
        return angle
        
    
        
                

