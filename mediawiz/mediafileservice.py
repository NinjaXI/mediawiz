'''
Created on 10 Dec 2018

@author: NinjaXI
'''

import os
import config
import util
import re

seriesSource = config.seriesSource
movieSource = config.movieSource

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
     
def getSeries(seriesString):
    seriesId, seriesName = seriesSource.findSeriesByCache(seriesString)
    if seriesId == -1 and seriesName == "":
        print("Not Cached")
        seriesList = seriesSource.findSeries(seriesString) # TODO handle series names with "." in
        found = False
        for series in seriesList:
            if series[1] == seriesString:
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
        seriesSource.saveToCache(seriesString, seriesName, seriesId)
          
    return [seriesId, getForcedSeriesName(seriesName).strip()]

def getEpisode(epPart, seriesId):
    regMatch = re.findall(r"(\d+)", epPart)
    seasonNr = int(regMatch[0])
    episodeNr = int(regMatch[1])
    episodeName = seriesSource.findEpisode(seasonNr, episodeNr, seriesId)
    return [seasonNr, episodeNr, episodeName]

def getEpisodeForAbsoluteNo(absEpNo, seriesId):
    return seriesSource.findEpisodeForAbsoluteNo(absEpNo, seriesId)

def getMovie(movieString, movieYear):
    requestedByYear = True
    movieName = ""
    movieList = movieSource.findMovie(movieString, movieYear)

    if movieYear == "":
        requestedByYear = False

    if requestedByYear and not len(movieList) > 0:
        movieList = movieSource.findMovie(movieString, "")
        requestedByYear = False

    if len(movieList) > 0:
        if movieList[0][0] == movieString:
            movieName = movieList[0][0]
            movieYear = str(movieList[0][1])
        else:
            if requestedByYear:
                movieList = movieList + movieSource.findMovie(movieString, "")

            for ind, movie in enumerate(movieList):
                print(str(ind) + ". " + movie[0] + " (" + movie[1] + ")")
            usrInd = input("Select the correct movie")
            try:
                movieName = str(movieList[int(usrInd)][0])
                movieYear = str(movieList[int(usrInd)][1])
            except:
                print("Not Int") # TODO ask again
    return [movieName, movieYear]
    
def renameFiles(scanList, scanFolders):
    for mediaFile in scanList:
        if os.path.isfile(mediaFile):
            mediaFileName = os.path.basename(mediaFile)
            print(mediaFileName)
            
            m = config.seasonEpRegex.search(mediaFileName)
            if m:
                seriesString = mediaFileName.split(m.group(0))[0].replace(".", " ").strip("_- ")
                try:
                    seriesId, seriesName = getSeries(seriesString)
                    try:
                        seasonNr, episodeNr, episodeName = getEpisode(m.group(0), seriesId)
                        newFilename = util.sanitiseFilename(config.seriesFormat % {"st" : seriesName, "sn" : str(seasonNr), 
                                                                           "en" : str(episodeNr).zfill(2), "et" : episodeName})
                        os.rename(mediaFile, os.path.join(os.path.dirname(mediaFile), newFilename + mediaFileName[mediaFileName.rindex("."):]))
                        # TODO logger.info("Renamed " + mediaFileName + " to " + newFilename + mediaFileName[mediaFileName.rindex("."):])
                        print(newFilename)
                    except:
                        print("ERROR : Cannot find episodeNr " + str(episodeNr) + " of seasonNr " + str(seasonNr) + " of " + seriesName + "(" + seriesId + ")")
                except:
                    print("ERROR : Cannot find " + seriesString)
            else:
                m = config.animeEpRegex.search(mediaFileName)
                if m:
                    seriesString = mediaFileName.split(m.group(0))[0].replace(".", " ").strip("_- ")
                    if seriesString.startswith("["):
                        seriesString = seriesString[seriesString.index("]") + 1:].strip("_- ")
                    try:
                        seriesId, seriesName = getSeries(seriesString)
                        try:
                            seasonNr, episodeNr, episodeName = getEpisodeForAbsoluteNo(m.groups()[0], seriesId)
                            newFilename = util.sanitiseFilename(config.seriesFormat % {"st" : seriesName, "sn" : str(seasonNr), 
                                                                            "en" : str(episodeNr).zfill(2), "et" : episodeName})
                            os.rename(mediaFile, os.path.join(os.path.dirname(mediaFile), newFilename + mediaFileName[mediaFileName.rindex("."):]))
                            # TODO logger.info("Renamed " + mediaFileName + " to " + newFilename + mediaFileName[mediaFileName.rindex("."):])
                            print(newFilename)
                        except:
                            print("ERROR : Cannot find episodeNr " + str(episodeNr) + " of seasonNr " + str(seasonNr) + " of " + seriesName + "(" + seriesId + ")")
                    except:
                        print("ERROR : Cannot find " + seriesString)
                else :
                    m = config.movieRegex.search(mediaFileName)
                    if m:
                        movieYear = ""
                        movieString = mediaFileName.split(m.group(0))[0].replace(".", " ").strip("_- ")
                        if len(m.group(0).split(".")[0].strip("()")) == 4:
                            movieYear = m.group(0).split(".")[0].strip("()")
                        movieName, movieYear = getMovie(movieString, movieYear)

                        if movieName == "":
                            print("ERROR : Cannot find " + movieString)
                        else:
                            newFilename = util.sanitiseFilename(config.movieFormat % {"mt" : movieName, "my" : movieYear})
                            if config.movieInFolder:
                                newFolderName = util.sanitiseFilename(config.movieFolderFormat % {"mt" : movieName, "my" : movieYear})
                                folderString = os.path.split(os.path.dirname(mediaFile))[1].split(m.group(0))[0].replace(".", " ").strip("_- ")
                                if folderString.startswith(movieString):
                                    os.rename(mediaFile, os.path.join(os.path.dirname(mediaFile), newFilename + mediaFileName[mediaFileName.rindex("."):]))
                                    newFolderName = os.path.join(os.path.split(os.path.dirname(mediaFile))[0], newFolderName)
                                    os.rename(os.path.dirname(mediaFile), newFolderName)
                                    print(newFilename)

                                    for fileName in os.listdir(newFolderName):
                                        if fileName != newFilename + mediaFileName[mediaFileName.rindex("."):]:
                                            os.remove(os.path.join(os.path.dirname(mediaFile), fileName))
                                else:
                                    os.mkdir(os.path.join(os.path.dirname(mediaFile), newFolderName))
                                    os.rename(mediaFile, os.path.join(os.path.join(os.path.dirname(mediaFile), newFolderName), 
                                                                                    newFilename + mediaFileName[mediaFileName.rindex("."):]))
                                    print(newFilename)
        else:
            print("Checking : " + mediaFile)
            renameFiles(util.listDirFullPath(mediaFile), False)
