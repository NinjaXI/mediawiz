'''
Created on 21 Oct 2018

@author: NinjaXI
'''

# TODO docstrings, for now normal comments

class BaseTvSource:
    # method that returns a list of results for a given search parameter for series name
    # list should be of format [seriesId, seriesName]
    # where seriesId is an identifier the source uses to find the series, later used to find specific episode information
    def findSeries(self, seriesName):
        raise NotImplementedError()
    
    # method that returns the episode name as string for a given episode number and seriesId
    def findEpisode(self, seasonNo, episodeNo, seriesId):
        raise NotImplementedError()