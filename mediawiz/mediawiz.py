'''
Created on 18 Oct 2018

@author: NinjaXI
'''

#TODO error logging
#TODO test moving files before they are reached
import sys
import logging
import config
from tvsources.tvdbsource import TvdbSource
from fileservices import tvfileservice

logger = logging.getLogger("mediawiz")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("mediawiz.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s"))
logger.addHandler(fh)

if len(sys.argv) > 1:
    scanList = sys.argv[1:]
else:
    print("usage: mediawiz.py <fileList>")
    sys.exit(2)

config.tvSource = TvdbSource()

tvfileservice.renameFiles(scanList, True)