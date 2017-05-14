"""
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sun May 14 02:46:53 2017
"""
# Description:
#==============================================================================
# START CODE
from uh_genexpfiles import *
logfile = uh_genexpfiles()
logfile['eeg'].write("Hello, this is EEG file")

print logfile['eeg'].name
print logfile['kin'].name