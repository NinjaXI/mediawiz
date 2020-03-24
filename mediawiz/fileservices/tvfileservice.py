'''
Created on 10 Dec 2018

@author: NinjaXI
'''

import os
import config
import util
import re

def getForcedSeriesName(seriesName):
    ret = seriesName
    try:
        with open("forcedNames.txt") as sCache:
            for line in sCache:
                if line.split("|")[0] == seriesName:
                    ret = line.split("|")[1]
                    break
    except:
        ret = ret
    return ret
     
def getSeries(seriesPart):
    seriesId, seriesName = config.tvSource.findSeriesByCache(seriesPart)
    if seriesId == -1 and seriesName == "":
        print("Not Cached")
        seriesList = config.tvSource.findSeries(seriesPart) # TODO handle series names with "." in
        found = False
        for series in seriesList:
            if series[1] == seriesPart:
                seriesId = str(series[0])
                seriesName = series[1]
                found = True
                break
            if not found:
                for ind, series in enumerate(seriesList):
                    print(str(ind) + ". " + series[1])
                usrInd = input("Select the correct show")
                try:
                    seriesId = str(seriesList[int(usrInd)][0])
                    seriesName = str(seriesList[int(usrInd)][1])
                except:
                    print("Not Int") # TODO ask again
        config.tvSource.saveToCache(seriesPart, seriesName, seriesId)
          
    return [seriesId, getForcedSeriesName(seriesName).strip()]

def getEpisode(epPart, seriesId):
    regMatch = re.findall("(\d+)", epPart)
    seasonNr = int(regMatch[0])
    episodeNr = int(regMatch[1])
    episodeName = config.tvSource.findEpisode(seasonNr, episodeNr, seriesId)
    return [seasonNr, episodeNr, episodeName]
    
def renameFiles(scanList, scanFolders):
    for mediaFile in scanList:
        if os.path.isfile(mediaFile):
            mediaFileName = os.path.basename(mediaFile)
            print(mediaFileName)
            
            m = config.seasonEpRegex.search(mediaFileName)
            if m:
                seriesPart = mediaFileName.split(m.group(0))[0].replace(".", " ").strip("_- ")
                
                try:
                    seriesId, seriesName = getSeries(seriesPart)
                    try:
                        seasonNr, episodeNr, episodeName = getEpisode(m.group(0), seriesId)
                        newFilename = util.sanitiseFilename(config.titleFormat % {"st" : seriesName, "sn" : str(seasonNr), 
                                                                           "en" : str(episodeNr).zfill(2), "et" : episodeName})
                        os.rename(mediaFile, os.path.join(os.path.dirname(mediaFile), newFilename + mediaFileName[mediaFileName.rindex("."):]))
                        # TODO logger.info("Renamed " + mediaFileName + " to " + newFilename + mediaFileName[mediaFileName.rindex("."):])
                        print(newFilename)
                        #x = input("PAUSE")
                    except:
                        print("ERROR : Cannot find episodeNr " + str(episodeNr) + " of seasonNr " + str(seasonNr) + " of " + seriesName + "(" + seriesId + ")")
                except:
                    print("ERROR : Cannot find " + seriesPart)
        else:
            print("Checking : " + mediaFile)
            renameFiles(util.listDirFullPath(mediaFile), False)
