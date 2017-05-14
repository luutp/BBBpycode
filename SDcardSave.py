"""
 Description: Copy Data from "Exp Data" folder to SD card
     
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sun May 14 09:57:06 2017
"""
#==============================================================================
# START CODE
import os
import uh_utils as uh
import gvar_def
gvar = gvar_def.gvar()
# Instantiate SD card object
sdcard = uh.sdcard(gvar.sdcardLabel)
print os.listdir(sdcard.expDataDirPath)
sdcard.save_expdata(gvar.expDataDirPath,sdcard.expDataDirPath)
uh.list_dirtree(sdcard.path)