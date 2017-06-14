"""
 Description:
     
     Serial communication for BBB
     
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Mon Jun  5 04:46:34 2017
"""
#==============================================================================
# START CODE
import Adafruit_BBIO.UART as UART
import serial
import time
#==============================================================================
class BBBserial(object):
    def __init__(self,uartname = 'UART1',baudrate = 9600):
        self._uartname = uartname.upper()
        self._baudrate = baudrate
        self.init()
    @property
    def name(self):
        return self._uartname
    @property
    def baudrate(self):
        return self._baudrate        
    @baudrate.setter
    def baudrate(self,val):
        self.baudrate = val
        self.init()
    @property
    def status(self):
        if self.port.isOpen():
            return 'Open'
        else:
            return 'Closed'
    @property
    def _BAUDRATES(self):
        # List of valide baurate values
        return self.port.BAUDRATES
    def init(self):    
        UART.setup(self.name)
        if self.name.lower() == 'uart1':
            self.port = serial.Serial(port='/dev/ttyO1',baudrate = self.baudrate)
        elif self.name.lower() == 'uart2':
            self.port = serial.Serial(port='/dev/ttyO2',baudrate = self.baudrate)
        elif self.name.lower() == 'uart3':
            self.port = serial.Serial(port='/dev/ttyO3',baudrate = self.baudrate)
        elif self.name.lower() == 'uart4':
            self.port = serial.Serial(port='/dev/ttyO4',baudrate = self.baudrate)
        elif self.name.lower() == 'uart5':
            self.port = serial.Serial(port='/dev/ttyO5',baudrate = self.baudrate)
        else:
            print 'Port: %s is not support' %self.name

#  Debug 
#==============================================================================
if __name__ == "__main__":
    myserial = BBBserial('UART1')
    print myserial.name
    print myserial.baudrate
    print myserial.status
#    print myserial._BAUDRATES
try:
    while(1):
        if myserial.port.isOpen():
            print 'Sending Data:'        
            myserial.port.write('Hello')
        else:
            print 'Port is closed'
        time.sleep(1)
except KeyboardInterrupt:
    print 'EXIT'
    myserial.port.close()
    UART.cleanup()        
#    print(dir(serial))
