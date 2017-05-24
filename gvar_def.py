"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sun May 14 07:40:19 2017
"""
# Description:
#==============================================================================
# START CODE
import os, inspect
# Currdir is the directory of THIS file
currdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#==============================================================================
class gvar():
    def __init__(self):
        self.expDataDirName = 'Exp Data'
        self.expDataDirPath = '/root/luu/' + self.expDataDirName
        self.sdcardLabel = 'BBB_SDCARD'
        self.sdcardPath = '/media/' + self.sdcardLabel   
        self.bbbPinmapfilename = 'bbbPinMap.txt' # txt file in curdir
        self.bbbPin = {} # Initate empty dictionary
        self.bbbPinDef()
        # BBB PIN map
    def bbbPinDef(self):
        txtfilepath = os.path.join(currdir,self.bbbPinmapfilename)
        # Open text file
        with open(txtfilepath) as fid:
            for line in fid:
                # Skip comment lines in txt file
                if (line[0] != '#'): 
                    # Split line by \t deliminiter
                    name, pinID, note = line.split('\t')                    
                    # Save to a dict variable
                    self.bbbPin[name] = pinID
        
        
