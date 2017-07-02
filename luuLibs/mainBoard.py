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
 
 .. figure:: luuLibs/icons/logo_uh.jpg
    :width: 280px
    :height: 80px
    :align: left
    
    **Department of Electrical & Computer Engineering**
    
    **Laboratory for Noninvasive Brain-Machine Interface Systems**
    
    `Facebook Page <https://www.facebook.com/UHBMIST/>`_
    
 Created on: *Sat Jul 01 16:48:44 2017*
 
 Python version: *2.7*
"""
#==============================================================================
# Import packages
#import Adafruit_BBIO.GPIO as GPIO
#import Adafruit_BBIO.ADC as ADC
import os, inspect
import utils
#==============================================================================
# DEFINE
DATADIRNAME = 'BBB Exp Data'
PINMAP_FILENAME = 'bbbPinMap.txt'
EXPFILE_TIMEKEY = '%y_%m_%d'

#==============================================================================
class mainBoard(object,utils.parentClass):
    def __init__(self, name = 'BBB'):
        self.name = name
        utils.make_dir(self.dataDir)
#==============================================================================
# ATTRIBUTES
#==============================================================================    
    @property
    def pycodeDir(self):
        thisDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        return os.path.dirname(thisDir)
    
    @property
    def dataDir(self):
        temp = os.path.join(os.path.dirname(self.pycodeDir), 
                            DATADIRNAME)
        return temp
    
    @property
    def subjList(self):
        return utils.get_subDir(self.dataDir,fullpath = False)      
        
    @property
    def pinmapFile(self):
        temp = os.path.join(self.pycodeDir, PINMAP_FILENAME)
        return temp
    
    @property
    def pinmap(self):
        # Open text file
        temp = {}
        with open(self.pinmapFile) as fid:
            for line in fid:
                # Skip comment lines in txt file
                if line and (line[0] != '#'): 
                    # Split line by \t deliminiter
                    partList = line.split('\t')                    
                    # Save to a dict variable
                    if len(partList) > 1: # Exclude empty line with ['\n']
                        temp[partList[0]] = partList[1]
        return temp
    
#==============================================================================
def get_bbbplatform():
    PLATFORM = ['BBB', 'BBB_WIFI'] # BBB or BBB_WIFI. option to set I2C bus.
    # Check if device is BBB or BBB Wifi with Wlan feature
    bbb = PLATFORM[0] # Default as BeagleBone black
    wifiInfo = '/proc/net/wireless'
    with open(wifiInfo) as fid:
        for line in fid:
            if 'wlan0' in line:
                bbb = PLATFORM[1]
    print('Device: {}'.format(bbb))
    return bbb

#==============================================================================
# FUNCTIONS
#==============================================================================
def make_expfiles(subjID, filetype = ['eeg']):
    '''
    '''
    myboard = mainBoard()
    # Create subject folder
    subjfullpath = os.path.join(myboard.dataDir,subjID)
    utils.make_dir(subjfullpath)
    # Create list of filenames
    trial = 0
    timestamp = utils.get_timenow(key = EXPFILE_TIMEKEY)
    tdayfileList = utils.get_files(subjfullpath,match = timestamp,
                                     fullpath = False)
    if tdayfileList:
        trialList = []
        for f in tdayfileList:
            expf = expFile(f)
            trialList.append(expf.trial)
        trial = max(trialList) + 1
    logfile = {}
    for ftype in filetype:
        temp = expFile(subjID = subjID,
                       trial = trial,
                       filetype = ftype)                       
        logfile[ftype] = open(os.path.join(subjfullpath,
                                        temp.filename),'w')
        
    return logfile

#==============================================================================
def get_expfiles(**kwargs):
    '''
        Get experiment data file names
        
        kwargs:
        #######
        :subjID: Subject ID
        :trial: trial number
        :timestamp: Default. Today
        :filetype: a keyword in exp filename
        :fullpath: Default. True
    '''
    # Parsers
    varargin = {'subjID': None,
                'trial': None,
                'timestamp': utils.get_timenow(key=EXPFILE_TIMEKEY),
                'filetype': None,
                'fullpath': True}        
    varargin = utils.get_varargin(varargin,kwargs)
    ####
    allfiles = [];
    myboard = mainBoard()
    for subj in myboard.subjList:
        subjfiles = get_subjfiles(subj)
        for f in subjfiles:
            allfiles.append(f)
    # Convert all files full path to filename
    filenames = [expFile(f) for f in utils.get_filename(allfiles)]
    output = filenames
    for key,val in varargin.items():
        if val is None:
            pass
        else:
            if key == 'subjID':
                output = [f for f in output if val == f.subjID]
            elif key == 'trial':
                trial = val
                if val == -1:
                    trialList = [f.trial for f in output]
                    trial = max(trialList)
                output = [f for f in output if trial == f.trial]
            elif key == 'timestamp':
                output = [f for f in output if val == f.timestamp]
            elif key == 'filetype':
                output = [f for f in output if val == f.filetype]
                
    if varargin['fullpath'] is True:
        output = [os.path.join(myboard.dataDir,f.subjID,f.filename)
                    for f in output]
    else:
        output = [f.filename for f in output]
    return output

#==============================================================================
def get_subjfiles(subjID):
    myboard = mainBoard()
    return utils.get_files(os.path.join(myboard.dataDir,subjID))
        
#==============================================================================
# RELEVANT CLASSES
#==============================================================================
class expFile(object,utils.parentClass):
    def __init__(self,*args,**kwargs):
        '''
            File class for experimental data.
            
            args:
            #####
            :fullfilename: full filename. Format subjID-timestamp-Trial-filetype
            kwargs:
            #######
            :subjID: Subject ID
            :trial: trial number
            :filetype: experimental data type 'eeg', 'kin','imu',etc
        '''
        if args:
            self.filename = args[0]
            return
        # Parsers
        varargin = {'subjID':'Anonymous',
                    'trial': 0,
                    'filetype': ''}        
        varargin = utils.get_varargin(varargin,kwargs)
        self.filename = '-'.join([varargin['subjID'], 
                                  utils.get_timenow(key=EXPFILE_TIMEKEY),
                                  'T{:02d}'.format(varargin['trial']),
                                    varargin['filetype'],
                                ])
    @property
    def timestamp(self):
        return self.get_fileInfo('timestamp')
    @property
    def subjID(self):
        return self.get_fileInfo('subjID')
    @property
    def trial(self):
        return self.get_fileInfo('trial')
    @property
    def filetype(self):
        return self.get_fileInfo('filetype')
#==============================================================================
    def get_fileInfo(self,*args):
        '''
        '''
        fileparts = self.filename.split('-')
        if not args:
            return fileparts
        else:
            if args[0].lower() == 'subjid':
                return fileparts[0]
            if args[0].lower() == 'timestamp':
                return fileparts[1]
            if args[0].lower() == 'trial':
                trialStr = fileparts[2]
                return int(trialStr[1:])
            if args[0].lower() == 'filetype':
                return fileparts[3]
            
    
#==============================================================================
def main():
    myboard = mainBoard()
    utils.printlist(get_expfiles(subjID = 'UH_AB_02'))
    myboard.print_Me()   
#==============================================================================
if __name__ == '__main__':
    main()
