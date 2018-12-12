'''
Created on 13 Nov 2018

@author: NinjaXI
'''

import re
import os

def listDirFullPath(path):
    return [os.path.join(path, file) for file in os.listdir(path)]

def sanitiseFilename(s):
    s = s.replace(":", "- ").replace("\\", " ").replace("/", " ")
    s = re.sub(r" +", " ", s)
    return re.sub(r"[^-'+)(\w\s.]", "", s)
