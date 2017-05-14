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