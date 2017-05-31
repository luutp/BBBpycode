"""
 Description:
     
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sun May 28 19:23:57 2017
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
        self.modemat = dict(zip(self.mode,(np.zeros([3,2]),np.zeros([3,5]))))
    @property
    def modephase(self):
        return dict(zip(self.mode,self.phase))    
    @property
    def state(self):
        return [0,0]    
    @property
    def stateIC(self):
        modeICmat = self.modemat[self.mode[self.state[0]]]
        stateIC = modeICmat[:,self.state[1]]
        return stateIC
    def setModeICmat(self, mode, modeICmat):
        # Set Impedent components for a given walking mode
        #           Phase1  Phase2  ...
        # Impedance
        # Damping
        # eqPos: Equilibrium position
        self.modemat[mode] = modeICmat
    def getModeICmat(self,mode = 'walk'):
        modeICmat = self.modemat[mode]
        return modeICmat
    def getstateIC(self):
        # IC of current state (walking mode, current phase)
        modeICmat = self.modemat[self.mode[self.state[0]]]
        stateIC = modeICmat[:,self.state[1]]
        return stateIC
    def getModePhaseName(self):
        # Print out all the walking mode and phases in each mode
        mode = self.mode[self.state[0]]
        allphase = self.modephase[mode]
        phase = allphase[self.state[1]]
        return mode,phase
    def update(self): 
        # Update current state based o foot sensors data.
        pass
    def stateupdate(self,stateInput):
        self.state = stateInput
        modeICmat = self.modemat[self.mode[self.state[0]]]
        stateIC = modeICmat[:,self.state[1]]
        self.stateIC = stateIC
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
    # WalkICmode obtained from Huang et al. paper
    walkICmode = np.array([[2, 3, 1, 1, 1],
                           [0.05, 0.05, 0.01, 0.01, 0.01],
                           [5, 10, 45, 60, 10]]);
    this.setModeICmat(this.mode[1],walkICmode)                           
    walkICmode = this.getModeICmat(mode = 'walk')
    print walkICmode
#    this.state = [1,2]   
    this.stateupdate([1,2])
    print this.state
    print this.modemat
    print this.stateIC
else:
    pass
