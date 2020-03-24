'''
Created on 10 Dec 2018

@author: NinjaXI
'''

import re
from tvsources.tvdbsource import TvdbSource

titleFormat = "%(st)s - %(sn)sx%(en)s - %(et)s" # TODO configurable
seasonEpRegex = re.compile(r"([sS]\d+[eE]\d+-\d+)|([sS]\d+[eE]\d+_\d+)|([sS]\d+[eE]\d+[eE]\d+)|([sS]\d+[eE]\d+)|(\d+x\d+)")
tvSource = TvdbSource()