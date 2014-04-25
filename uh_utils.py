"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sun May 14 00:55:34 2017
"""
# Description: A utilities module that designed for BBB
# Classes included: uh_FileIO
#==============================================================================
# START CODE
# Import packages and define global varirbales
import datetime
import pytz
import os
import shutil # For copy files
import gvar_def
from scipy.signal import butter, tf2ss
import numpy.matlib as np # Use version later than 1.10
gvar = gvar_def.gvar()
expDataDirName = gvar.expDataDirName #'Exp Data'
expDataDirPath = os.path.join(os.path.abspath(os.pardir),expDataDirName)
sdcardLabel = gvar.sdcardLabel #'BBB_SDCARD'
sdcardPath = os.path.join('/media',sdcardLabel)
sdcardDataDirPath = os.path.join(sdcardPath,expDataDirName)
#==============================================================================
class sdcard:
    def __init__(self,label=sdcardLabel):
        self.label = label
        self.path = os.path.join('/media',self.label)
        self.expDataDirPath = os.path.join(self.path,expDataDirName)
        self.make_expDataDir();
    def save_expdata(self,source_folder = expDataDirPath,destination_folder = sdcardDataDirPath):        
        if not os.path.isdir(destination_folder):
            print 'MAKE: Dir %s' % destination_folder
            os.mkdir(destination_folder)
        for root, dirs, files in os.walk(source_folder):
            for item in dirs:
                dst_path = os.path.join(destination_folder,item)
                if not os.path.exists(dst_path):
                    print 'MAKE: Dir %s' % dst_path
                    os.mkdir(dst_path)
                    
            for item in files:
                src_path = os.path.join(root,item)
                ignore,temp = os.path.split(root)
                dst_path = os.path.join(destination_folder, temp)                
                shutil.copy2(src_path, dst_path)
                print 'SAVED: %s' % os.path.join(dst_path,item)
        print 'DONE: Move Experimental Data to SD card'
    def cleanup(self):
        shutil.rmtree(self.expDataDirPath)
        print 'SD card: %s' % os.listdir(self.path)
    def make_expDataDir(self):
        # Make Exp Data folder
        if not os.path.isdir(self.expDataDirPath):
            print 'MAKE: Dir %s on SD Card' %(expDataDirName)
            os.mkdir(self.expDataDirPath)
#==============================================================================
class FileIO:
    def __init__(self,
                 expDataDirName = 'Exp Data', 
                 subjID = 'UH_AB_01',
                 logfilekey = ['eeg','kin']):
#        Initiate data dir and subjID
        self.expDataDirName = expDataDirName
        self.subjID = subjID
        self.logfileKey = logfilekey
        self.subjDirPath = self.get_subjdir()
    def get_subjdir(self):
        currdir = os.path.abspath(os.path.curdir)
        rootdir,temp = os.path.split(currdir)  # luu dir
        self.expDataDirPath = os.path.join(rootdir,self.expDataDirName) # luu\Exp Data dir
        subjDirPath = os.path.join(self.expDataDirPath,self.subjID)
        self.subjDirPath = subjDirPath
        return subjDirPath
    #####    
    def make_expfiles(self):        
        # Working and data directories
        subjDirPath = self.subjDirPath
        subjID = self.subjID
        logfileKey = self.logfileKey # python list
        tdaystr = get_today();
        # Make Subject Folder
        if not os.path.isdir(subjDirPath):
            print 'Make: %s folder' %(subjID)
            os.mkdir(subjDirPath)
        # Create txt data files
        trial = 0
        filelist = [f for f in os.listdir(subjDirPath) if os.path.isfile(os.path.join(subjDirPath,f))]
        tdayfilelist = [f for f in filelist if f.find(tdaystr)!=-1]
        # Find latest trial in subject folder
        if tdayfilelist:
            triallist = [];
            for thisfile in tdayfilelist:
                marker = thisfile.find('T');
                triallist.append(int(thisfile[marker+1:marker+3]))        
            trial = max(triallist) + 1
        # Create filename            
        logfile = {} # python dict
        for key in logfileKey:
            logfilename = '%s-T%.2d-%s-%s.txt' %(subjID,trial,tdaystr,key)
            logfile[key] = open(os.path.join(subjDirPath,logfilename),'w');
        self.logfile = logfile
        return logfile        
#==============================================================================
def get_today():
#        Datetime data
        temp = datetime.datetime.now(pytz.timezone('US/Central'))
        tday = temp.strftime('%y-%m-%d')        
        return tday
#==============================================================================
def rmdir(inputDir):
        if os.path.isdir(inputDir):
            shutil.rmtree(inputDir)
            print 'Remove: %s Directory' % inputDir
            list_dirtree(os.path.dirname(inputDir))
        else:
            print 'Not Exist: % Directory' % inputDir
#==============================================================================
def savetoSDcard():
    mysdcard = sdcard(gvar.sdcardLabel)            
    mysdcard.save_expdata()    
#==============================================================================
def list_dirtree(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
#==============================================================================
# Attribute display class: Use this as a parent class to overload print method            
#==============================================================================
class AttrDisplay:
    '''
    Use this as a parent class to overload display method for class.\n
    '''
    def gatherAttrs(self):
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append('%s=%s' % (key, getattr(self, key)))
        return ', '.join(attrs)
    def __str__(self):
        return '[%s: %s]' % (self.__class__.__name__, self.gatherAttrs())

#==============================================================================
# Signal processor
#==============================================================================
class uh_filter():
    '''
    #====DESCRIPTION:\n
    Filter raw signal in real time manner, 1 input, 1 output.\n
    Note: Instantiate the filter before while() or for loop.\n
    #====INPUT:\n
    order: order of Butterworth filter. The larger, the stronger attenuation but longer time delay.\n
    cutoff: Take scalar value for high and low-pass fitler, 2-element vector if band-pass filter is used.\n
    Fs: Sampling frequency of raw signal.\n    
    filtertype: 'low', 'high', or 'bandpass'
    '''
    def __init__(self,order,cutoff,Fs,filtertype):
        self.order = order
        self.Fs = Fs
        self.Wn = self.Fs*0.5 # Time 0.5 to create float type
        self.type = filtertype;
        self.num, self.den = butter(self.order,np.divide(cutoff,self.Wn),self.type)
        self.A, self.B, self.C, self.D = tf2ss(self.num,self.den)
        self.Xnn = np.zeros((np.size(self.A,1),1))
    def applyFilter(self,inputSig):
        if np.size(inputSig) == 1: 
            u = inputSig # Handle scalar case
            myXnn = self.Xnn # get current state
            self.Xnn = np.add(np.matmul(self.A,myXnn), self.B*u) # State updated
            ytemp = np.add(np.matmul(self.C,myXnn), self.D*u)
            filtSig = np.asscalar(ytemp)
        else: 
            filtSig = [0]*(np.size(inputSig),1)
            for i in range(np.size(inputSig)):    
                u = inputSig[i]
                myXnn = self.Xnn # get current state
                self.Xnn = np.add(np.matmul(self.A,myXnn), self.B*u) # State updated
                ytemp = np.add(np.matmul(self.C,myXnn), self.D*u)
                filtSig[i] = ytemp.tolist()            
        return filtSig
#==============================================================================
def quickif(cond, trueval, falseval):
    '''
    ifcond is true then retun trueval, 
    
    else return false val
    '''
    if cond:
        return trueval
    else:
        return falseval
#==============================================================================
# Debug 
#==============================================================================
if __name__ == "__main__":
else:
    pass    