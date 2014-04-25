"""
 Description:
     
     Finite state impedence controller for powered knee prosthetic leg.
     
     Include: Finite State machine class for gait phase transition rule
     
     An impedance controller to compute torque and current
     
     
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Thu Apr 24 04:00:14 2014
"""
#==============================================================================
# START CODE
import math as math
import numpy as np
#==============================================================================
class FSM():
    '''
    Finite State Machine Class
    
    '''
    def __init__(self,mode = ['stand'], phase = (['bearing','non-bearing'],)):
        '''
        mode: walking mode, 'stand', 'walk', 'upstair'. List
        
        Phase: phases in a walking mode. Tuple
        '''
        # Locomotion mode or walking terrain
        self.mode = mode
        self.phase = phase
        standmat = np.zeros([3,2])
        walkmat = np.zeros([3,5])
        self.modephase = dict(zip(self.mode,self.phase))    
        self.modemat = dict(zip(self.mode,(standmat,walkmat)))
        self.state = [0,0]
    def getModePhaseName(self):
        mode = self.mode[self.state[0]]
        allphase = self.modephase[mode]
        phase = allphase[self.state[1]]
        return mode,phase
    def update(self): 
        pass
#==============================================================================
class impedanceController(dict):
    '''
    Impedance controller class for Finite State Impedance control of prosthetic leg
    '''
    def __init__(self, stiffness = 1, damping = 0.01, eq_pos = 10):
        '''
        stiffness and damping of human walking dynamic
        
        eq_pos: equilibrium position        
        '''        
        self.keys = ['stiffness','damping','eqPos']
        # Init params attribute dict
        vals = [stiffness, damping, eq_pos]   
        self.params = dict(zip(self.keys,vals))
        # Create threshold dict attribute
        thres = [[1.6, 2.2], [0.01, 0.1],[4, 10]]
        self.threshold = dict(zip(self.keys,thres))
    def setParams(self,*args,**kwargs):
       '''
       setParams(params_input)
       
       setParams(stiffness,damping,eqPos)
       
       setParams(stiffness=val, damping=val,eqPos=val)
       '''     
       # If a dict or args are given
       if len(args) != 0:
           for idx, arg in enumerate(args):
               if type(arg) is dict:
                   for key,val in arg.items():
                       self.params[key] = val
                   return           
               else:
                   self.params[self.keys[idx]] = arg
           return                   
       # If keyword arguments are given
       for key,val in kwargs.iteritems():
           keyset = 0 # Flag to check if keyword is correct
           for mykey in self.keys:
               if key == mykey:
                   self.params[mykey]=val
                   keyset = 1
                   break        
           if keyset == 0:
               print "WARNING: Keyword argument is not match. Use:"
               print self.keys               
#==============================================================================
    def setThreshold(self,*args,**kwargs):
       '''
       setThreshold(params_input)
       
       setThreshold(stiffness,damping,eqPos)
       
       setThreshold(stiffness=val, damping=val,eqPos=val)
       '''     
       # If a dict or args are given
       if len(args) != 0:
           for idx, arg in enumerate(args):
               if type(arg) is dict:
                   self.threshold = arg
                   return           
               else:
                   self.threshold[self.keys[idx]] = arg
           return                   
       # If keyword arguments are given
       for key,val in kwargs.iteritems():
           keyset = 0 # Flag to check if keyword is correct
           for mykey in self.keys:
               if key == mykey:
                   self.threshold[mykey]=val
                   keyset = 1
                   break        
           if keyset == 0:
               print "WARNING: Keyword argument is not match. Use:"
               print self.keys               
#==============================================================================
    def computeTorque(self,jointangle,jointvel):
        '''
        Compute joint torque
        '''
        stiffness = self.params[self.keys[0]]        
        damping = self.params[self.keys[1]]
        eqPos = self.params[self.keys[2]]
        self.torque = stiffness*math.radians(jointangle-eqPos) + damping*jointvel
        return self.torque
#==============================================================================
#  Debug 
#==============================================================================
if __name__ == "__main__":
    mode = ['stand','walk']
    phase = (['bearing','nonbearing'],['IDS','SS','TDS','SWF','SWE'])
    this = FSM(mode,phase)    
    print this.mode
    print this.phase
    print this.modephase
    print this.modemat
    print this.getModePhaseName()
    this.state = [1,2]
    print this.getModePhaseName()
else:
    pass
        