'''
Created on 18 Oct 2018

@author: NinjaXI
'''

#TODO error logging
import os
import re
import sys
import logging
from tvsources.tvdbsource import TvdbSource
import util

logger = logging.getLogger("mediawiz")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("mediawiz.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s"))
logger.addHandler(fh)

scanDir = ""
try:
    scanDir = sys.argv[1]
except:
    print("usage: mediawiz.py <inputfolder>")
    #scanDir = "../../#testfolder/" #for testing
    sys.exit(2)
    
if not os.path.exists(scanDir):
    print("Path does not exist : " + scanDir)
    #scanDir = "../../#testfolder/" #for testing
    sys.exit(2)

titleFormat = "%(st)s - %(sn)sx%(en)s - %(et)s" # TODO configurable

tvSource = TvdbSource()

seasonEpRegex = re.compile("([sS]\d+[eE]\d+-\d+)|([sS]\d+[eE]\d+_\d+)|([sS]\d+[eE]\d+[eE]\d+)|([sS]\d+[eE]\d+)|(\d+x\d+)")

print("Checking : " + scanDir)
for mediaFile in os.listdir(scanDir):
    if os.path.isfile(os.path.join(scanDir, mediaFile)):
        print(mediaFile)
        
        # initialize strings for later use
        seriesName = ""
        seriesId = ""
        seasonNr = ""
        episodeNr = ""
        episodeName = ""
        
        m = seasonEpRegex.search(mediaFile)
        if m:
            titlePart = mediaFile.split(m.group(0))[0]
            try:
                seriesList = tvSource.findSeries(titlePart.replace(".", " ")) # TODO handle series names with "." in
                found = False
                for series in seriesList:
                    if series[1] == titlePart.replace(".", " ").strip():
                        seriesId = str(series[0])
                        seriesName = series[1]
                        found = True
                        break;
                    if not found:
                        for ind, series in enumerate(seriesList):
                            print(str(ind) + ". " + series[1])
                        #usrInd = "0" #for testing
                        usrInd = input("Select the correct show")
                        try:
                            seriesId = str(seriesList[int(usrInd)][0])
                            seriesName = str(seriesList[int(usrInd)][1])
                        except:
                            print("Not Int") # TODO ask again
                regMatch = re.findall("(\d+)", m.group(0))
                seasonNr = int(regMatch[0])
                episodeNr = int(regMatch[1])
                try:
                    episodeName = tvSource.findEpisode(seasonNr, episodeNr, seriesId)
                    newFilename = util.sanitiseFilename(titleFormat % {"st" : seriesName, "sn" : str(seasonNr), 
                                                                       "en" : str(episodeNr).zfill(2), "et" : episodeName})
                    os.rename(os.path.join(scanDir, mediaFile), os.path.join(scanDir, newFilename + mediaFile[mediaFile.rindex("."):]))
                    logger.info("Renamed " + mediaFile + " to " + newFilename + mediaFile[mediaFile.rindex("."):])
                    print(newFilename)
                except:
                    print("ERROR : Cannot find episodeNr " + str(episodeNr) + " of seasonNr " + str(seasonNr) + " of " + seriesName + "(" + seriesId + ")")
            except:
                print("ERROR : Cannot find " + titlePart.replace(".", " "))
        