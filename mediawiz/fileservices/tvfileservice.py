'''
Created on 10 Dec 2018

@author: NinjaXI
'''

import os
import config
import util
import re

def renameFiles(scanList, scanFolders):
    for mediaFile in scanList:
        if os.path.isfile(mediaFile):
            mediaFileName = os.path.basename(mediaFile)
            print(mediaFileName)
            
            # initialize strings for later use
            seriesName = ""
            seriesId = ""
            seasonNr = ""
            episodeNr = ""
            episodeName = ""
            
            m = config.seasonEpRegex.search(mediaFileName)
            if m:
                titlePart = mediaFileName.split(m.group(0))[0]
                try:
                    seriesList = config.tvSource.findSeries(titlePart.replace(".", " ")) # TODO handle series names with "." in
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
                        episodeName = config.tvSource.findEpisode(seasonNr, episodeNr, seriesId)
                        newFilename = util.sanitiseFilename(config.titleFormat % {"st" : seriesName, "sn" : str(seasonNr), 
                                                                           "en" : str(episodeNr).zfill(2), "et" : episodeName})
                        os.rename(mediaFile, os.path.join(os.path.dirname(mediaFile), newFilename + mediaFileName[mediaFileName.rindex("."):]))
                        #logger.info("Renamed " + mediaFileName + " to " + newFilename + mediaFileName[mediaFileName.rindex("."):])
                        print(newFilename)
                    except:
                        print("ERROR : Cannot find episodeNr " + str(episodeNr) + " of seasonNr " + str(seasonNr) + " of " + seriesName + "(" + seriesId + ")")
                except:
                    print("ERROR : Cannot find " + titlePart.replace(".", " "))
        else:
            print("Checking : " + mediaFile)
            renameFiles(util.listDirFullPath(mediaFile), False)