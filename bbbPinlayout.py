# -*- coding: utf-8 -*-

#==============================================================================
"""
 Created on Sat May 13 02:53:47 2017
 
 @author: Trieu Phat Luu
 
 Email: tpluu2207@gmail.com
"""
# 
# Description:
#     
# Input:
    
# Output
#==============================================================================

# START CODE

import os 
currdir = os.getcwd()
docdir = "/root/luu/Documents"
txtfile = docdir + "/bbbPinout.txt"
# Open text file
with open(txtfile) as fid:
    for line in fid:
        print line