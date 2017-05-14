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
#from uh_genexpfiles import *
#from uh_utils import *
import uh_utils as uh
myfileio = uh.FileIO('Exp Data','UH_AB_01',['eeg'])
mytime = uh.timenow()
print uh.timenow().tday
print myfileio.subjdir


#logfile = uh_genexpfiles()
#logfile['eeg'].write("Hello, this is EEG file")
#print logfile['eeg'].name
#import numpy.matlib as np
#from scipy.signal import butter
#import matplotlib.pyplot as plt
#x = np.linspace(0,10,20)
#y = np.power(x,2)
#plt.plot(x,y)
#plt.show()
#print "DONE"

#a = np.array([1,2,3])
##b = np.array([4,5,6])
#unitmat = 2*np.eye(3);
#print np.size(unitmat,1)