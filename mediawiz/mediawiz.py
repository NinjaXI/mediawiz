'''
Created on 18 Oct 2018

@author: NinjaXI
'''

import os
import re
from tvsources.tvdbsource import TvdbSource

scanDir = "../../#testfolder/" # TODO input/working dir
titleFormat = "$st - $snx$en - $et" # TODO configurable

tvSource = TvdbSource()

seasonEpRegex = re.compile("([sS]\d+[eE]\d+-\d+)|([sS]\d+[eE]\d+_\d+)|([sS]\d+[eE]\d+[eE]\d+)|([sS]\d+[eE]\d+)|(\d+x\d+)")

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
                seriesList = tvSource.findSeries(titlePart.replace(".", " "))
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
                        usrInd = "0"
                        #usrInd = input("Select the correct show") # commented for testing
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
        print(titleFormat.replace("$st", seriesName).replace("$sn", str(seasonNr)).replace("$en", str(episodeNr).zfill(2)).replace("$et", str(episodeName)))