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
        self.expDataDirName = 'Exp Data'
        self.expDataDirPath = '/root/luu/' + self.expDataDirName
        self.sdcardLabel = 'BBB_SDCARD'
        self.sdcardPath = '/media/' + self.sdcardLabel   
        # BBB PIN map
        self.bbbPIN['SwitchFW'] = "P9_27"
    
