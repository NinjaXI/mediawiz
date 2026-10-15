'''
Created on 21 Oct 2018

@author: NinjaXI
'''

# TODO docstrings, for now normal comments

class BaseMediaSource:
    # returns a list of results for a given search parameter for series name
    # list should be of format [seriesId, seriesName]
    # where seriesId is an identifier the source uses to find the series, later used to find specific episode information
    def findSeries(self, seriesName):
        raise NotImplementedError()
    
    # returns the episode name as string for a given episode number and seriesId
    def findEpisode(self, seasonNo, episodeNo, seriesId):
        raise NotImplementedError()

    # returns the season number, episode number and episode name as string for a given absolute episode number and seriesId        
    def findEpisodeForAbsoluteNo(self, absoluteEpisodeNo, seriesId):
        raise NotImplementedError()

    # returns the episode name as string for a given episode number and seriesId from cache if cache supported
    def findSeriesByCache(self, seriesName):
        raise NotImplementedError()

    # saves seriesName and id to cache if implemented
    def saveToCache(self, seriesName, seriesId):
        print("No Cache")

    def findMovie(self, movieName, movieYear):
        raise NotImplementedError()
