'''
Created on 13 Nov 2018

@author: NinjaXI
'''

import re

def sanitiseFilename(s):
    s = s.replace(":", "- ").replace("\\", " ").replace("/", " ")
    s = re.sub(r" +", " ", s)
    return re.sub(r"[^-'+)(\w\s.]", "", s)
