'''
Created on 18 Oct 2018

@author: NinjaXI
'''

import os
import re
import sys
from tvsources.tvdbsource import TvdbSource

scanDir = ""
try:
    scanDir = sys.argv[1]
except:
    print("usage: mediawiz.py <inputfolder>")
    #scanDir = "..\..\#testfolder\test" #for testing
    sys.exit(2)
    
if not os.path.exists(scanDir):
    print("Path does not exist : " + scanDir)
    #scanDir = "..\..\#testfolder\test" #for testing
    sys.exit(2)

titleFormat = "$st - $snx$en - $et" # TODO configurable

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
                except:
                    print("ERROR : Cannot find episodeNr " + str(episodeNr) + " of seasonNr " + str(seasonNr) + " of " + seriesName)              
            except:
                print("ERROR : Cannot find " + titlePart.replace(".", " "))
        newFilename = titleFormat.replace("$st", seriesName).replace("$sn", str(seasonNr)).replace("$en", str(episodeNr).zfill(2)).replace("$et", str(episodeName))
        print(scanDir + "\\" + newFilename)