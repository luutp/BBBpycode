# -*- coding: utf-8 -*-
"""
Descriptions
#############
Function description

:param: input argument
:returns: output
:Example:

.. Note::
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.    

.. seealso::    

Authors
#######
 Trieu Phat Luu. *Email: tpluu2207@gmail.com*
 
 .. figure:: icons/logo_uh.jpg
    :width: 280px
    :height: 80px
    :align: left
    
    **Department of Electrical & Computer Engineering**
    
    **Laboratory for Noninvasive Brain-Machine Interface Systems**
    
    `Facebook Page <https://www.facebook.com/UHBMIST/>`_
    
 Created on: *Sat Jul 01 03:08:42 2017*
 
 Python version: *2.7*
"""
#==============================================================================
# Import packages
import os, shutil
import inspect
import glob
import datetime, pytz

#==============================================================================
# DEFINE
thisDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#==============================================================================
# FILE IO
#==============================================================================
def make_dir(inputDir):
    if not os.path.isdir(inputDir):
        print('MAKE: Dir {}'.format(inputDir))
        os.makedirs(inputDir)
    
#==============================================================================
def del_dir(inputDir):
    if os.path.isdir(inputDir):
        shutil.rmtree(inputDir)
        print 'Remove: %s Directory' % inputDir
        list_dirtree(os.path.dirname(inputDir))
    else:
        print 'Not Exist: % Directory' % inputDir    

#==============================================================================
def del_files(fileList):
     # Get the most current data file or input filename
    for f in fileList:
        os.remove(f)

#==============================================================================
def list_dirtree(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))        
#==============================================================================
def get_thisDir():
    '''
    Return directory that contains this .py file
    '''
    thisDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return thisDir

#==============================================================================
def get_parentDir(inputDir, level = 1):
    '''
    This function returns parent directory for a given path
     :inputDir: Input directory
     :level: Level of parent directory. Default: 1
     :returns: parent directory
    '''
    parDir = inputDir
    for i in range(level):
        parDir = os.path.dirname(parDir)    
    return parDir

#==============================================================================
def get_subDir(inputDir,**kwargs):    
    '''
    Returns all sub directories of a given input directory
    '''
     # Parsers
    varargin = get_varargin({'fullpath': True},kwargs)
    print('{}({})'.format(inspect.stack()[0][3],varargin))
    subdirList = glob.glob(inputDir + "/*/")
    output = []
    for subdir in subdirList:
        if varargin['fullpath'] is True:            
            output.append(os.path.dirname(subdir))
        else:
            output.append(subdir.split('\\')[-2])
    return output

#==============================================================================
def get_files(inputDir, **kwargs):
    '''
    Get list of filenames in a given directories
     :Input: 
         * inputDir: Full path of given directory as input
     :Options:
         * filetype: default: None, select all files.
         * match: select filenames that matched with keywords.
     :Output:
         List of filenames
    '''
    # Parsers
    varargin = {'filetype':None,
                'match': None,
                'fullpath': True}        
    if kwargs: # if no input is given
        varargin.update((key, kwargs[key])
                        for key in varargin.keys()
                            if key in kwargs
                        )
    print('{}({})'.format(inspect.stack()[0][3],varargin))
    # Select file with given filetype
    if varargin['filetype'] is None:
        fileList = []
        for filename in os.listdir(inputDir):
            fileList.append(os.path.join(inputDir,filename))
    else:
        fileList = glob.glob(inputDir +"/*" + varargin['filetype'])
    # Only select file that matched with given keywords
    if varargin['match'] is None:
        matchList = fileList
    else:
        matchList = []
        for fullpath in fileList:
            nah,filename = os.path.split(fullpath)
            if varargin['match'].lower() in filename.lower():
                matchList.append(fullpath)
    # Return full path or filename
    if varargin['fullpath'] is True:
        output = matchList
    else:
        output = get_filename(matchList)
    return output

#==============================================================================
def get_filename(fullpathList):
    output = []
    for fullfile in fullpathList:
        nah, temp = os.path.split(fullfile)
        output.append(temp)
    return output
#==============================================================================
# USER IO
#==============================================================================
def printlist(inputlist):
    if not inputlist:
        print('[]')
    else:
        for el in inputlist:
            print('{}'.format(el))   
        
#==============================================================================
def printdict(dictin={}):
    for key, val in dictin.iteritems():
        print(key,val)   
        
#==============================================================================
def print_stack():
    print('{}- Running: {}...'.format(get_timenow('%H:%M:%S'),
          inspect.stack()[1][3]),
          )   
      
#==============================================================================
def get_timenow(key='%H:%M:%S'):
    '''
    %Y : YY; %m: mm; %d: dd
    %H : Hour; %M: Minute; %S: Seconds
    '''
    timenow = datetime.datetime.now(pytz.timezone('US/Central'))
    return timenow.strftime(key)  

def get_varargin(varargin,kwargs):
    '''
    Return variable input
    '''
    if kwargs:    
        varargin.update((key, kwargs[key])
                        for key in varargin.keys()
                        if key in kwargs
                        )
    return varargin
#==============================================================================
# CLASS
#==============================================================================
class parentClass():
    def get_Attrs(self):
            attrDict = {}
            for attr in dir(self):
                if '_' not in attr:
                    attrDict[attr] = getattr(self,attr)
            return attrDict
        
    def __str__(self):
        '''
        Overiding __str__ function to show all attributes
        '''
        attrDict = self.get_Attrs()
        attrs = []
        for key, val in attrDict.items():
            attrs.append('%s: %s' %(key, val))
        return ', '.join(attrs)
    
    def print_Me(self):
        for key, val in self.get_Attrs().items():
            print(key,val)
#==============================================================================
# OTHERS
#==============================================================================
def quickif(cond, trueval, falseval):
    '''
    ifcond is true then retun trueval, 
    
    else return false val
    '''
    if cond:
        return trueval
    else:
        return falseval
    
#==============================================================================
def main():
    pycodeDir = get_parentDir(thisDir,level=1)
    printlist(get_files(pycodeDir, filetype='.py',match='SDcard'))
    
#==============================================================================
if __name__ == '__main__':
    main()
