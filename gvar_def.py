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
class gvar:
    def __init__(self):
        gvar.expDataDirName = 'Exp Data'
        gvar.expDataDirPath = '/root/luu/' + gvar.expDataDirName
        gvar.sdcardLabel = 'BBB_SDCARD'
        gvar.sdcardPath = '/media/' + gvar.sdcardLabel        
    
