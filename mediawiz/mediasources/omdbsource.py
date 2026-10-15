'''
Created on 24 Mar 2018

@author: NinjaXI
'''

import requests
from mediasources.basemediasource import BaseMediaSource

class OmdbSource(BaseMediaSource):
    def __init__(self, apiKey):
        #http://www.omdbapi.com/?i=tt3896198&apikey=<apiKey>
        self.apiurl = "http://www.omdbapi.com/"
        self.apikey = apiKey
    
    def findMovie(self, movieName, movieYear):
        #TODO handle not found
        retList = []

        r = requests.get(self.apiurl + "?apikey=" + self.apikey + "&s=" + movieName + "&y=" + movieYear + "&type=movie")

        if r.status_code == 200:
            if "Error" in r.json():
                return retList

            for i in r.json()["Search"] :
                retList.append([i["Title"], i["Year"]])
            return retList
        else:
            raise BaseException()