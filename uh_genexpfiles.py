"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sun May 14 00:55:34 2017
"""
# Description:
#==============================================================================
# START CODE
# Import packages and define global varirbales
import datetime
import pytz
import os
expDataDir = 'Exp Data'
subjID = 'UH_AB_01'
# --------
def uh_genexpfiles():
    # Datetime format
    tday = datetime.datetime.now(pytz.timezone('US/Central'))
    tdaystr= tday.strftime('%y-%m-%d')
    # Working and data directories
    currdir = os.path.abspath(os.path.curdir);
    rootdir,temp = os.path.split(currdir)  # luu dir
    datadir = os.path.join(rootdir,expDataDir) # luu\Exp Data dir
    subjdir = os.path.join(datadir,subjID)
    # Make Subject Folder
    if not os.path.isdir(subjdir):
        print 'Make: %s folder' %(subjID)
        os.mkdir(subjdir)
        
    # Create txt data files
    trial = 0
    filelist = [f for f in os.listdir(subjdir) if os.path.isfile(os.path.join(subjdir,f))]
    tdayfilelist = [f for f in filelist if f.find(tdaystr)!=-1]
    # Find latest trial in subject folder
    if tdayfilelist:
        triallist = [];
        for thisfile in tdayfilelist:
            marker = thisfile.find('T');
            triallist.append(int(thisfile[marker+1:marker+3]))        
        trial = max(triallist) + 1
    # Create filename    
    logfilekey = ['eeg','kin'] # python list
    logfile = {} # python dict
    for key in logfilekey:
        logfilename = '%s-T%.2d-%s-%s.txt' %(subjID,trial,tdaystr,key)
        logfile[key] = open(os.path.join(subjdir,logfilename),'w');
    return logfile