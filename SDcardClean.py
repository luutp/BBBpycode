"""
 Description:
     
 Author: Trieu Phat Luu
 
 Lab for Non-invasive Brain-Machine Interface systems,
 University of Houston, 
 
 Email: tpluu2207@gmail.com
 
 Created on Sun May 14 10:38:11 2017
"""
#==============================================================================
# START CODE
import uh_utils as uh
import gvar_def
gvar = gvar_def.gvar()
# Instantiate SD card object
sdcard = uh.sdcard(gvar.sdcardLabel)
sdcard.cleanup()
uh.list_dirtree(sdcard.path)