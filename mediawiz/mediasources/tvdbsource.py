'''
Created on 21 Oct 2018

@author: NinjaXI
'''

import requests
from mediasources.basemediasource import BaseMediaSource

class TvdbSource(BaseMediaSource):
    def __init__(self, apiKey):
        self.apiurl = "https://api.thetvdb.com/"
        
        r = requests.post(self.apiurl + "login", json = {"apikey": apiKey}, headers = {"Content-Type":"application/json", "Accept":"application/json"})
        self.jwttoken = r.json()["token"]
        self.headers = {"Content-Type":"application/json", "Accept":"application/json", "Authorization":"Bearer " + self.jwttoken}
        # TODO refresh token timing
    
    def findSeries(self, seriesName):
        retList = []
                
        r = requests.get(self.apiurl + "search/series", params = {"name":seriesName}, headers = self.headers)
        
        if r.status_code == 200:
            for i in r.json()["data"] :
                retList.append([i["id"], i["seriesName"]])
            return retList
        else:
            raise BaseException()
            
    def findEpisode(self, seasonNo, episodeNo, seriesId):
        r = requests.get(self.apiurl + "series/" + str(seriesId) + "/episodes/query", params = {"airedSeason":seasonNo, "airedEpisode":episodeNo}, headers = self.headers)

        if r.status_code == 200:
            return r.json()["data"][0]["episodeName"]
        else:
            raise BaseException()
            
    def findEpisodeForAbsoluteNo(self, absoluteEpisodeNo, seriesId):
        r = requests.get(self.apiurl + "series/" + str(seriesId) + "/episodes/query", params = {"absoluteNumber": absoluteEpisodeNo}, headers = self.headers)

        if r.status_code == 200:
            r = requests.get(self.apiurl + "episodes/" + str(r.json()["data"][0]["id"]), headers = self.headers)

            if r.status_code == 200:
                return r.json()["data"]["airedSeason"], r.json()["data"]["airedEpisodeNumber"], r.json()["data"]["episodeName"]
            else:
                raise BaseException()
        else:
            raise BaseException()
        
    def findSeriesByCache(self, seriesName):
        try:
            with open("tvdbCache.txt") as sCache:
                for line in sCache:
                    if line.split("|")[0] == seriesName:
                        return [line.split("|")[2].strip(), line.split("|")[1].strip()]
        except:
            return [-1, ""] 
        return [-1, ""]
    
    def saveToCache(self, searchName, seriesName, seriesId):
        try:
            with open("tvdbCache.txt", "a") as sCache:
                sCache.write(searchName + "|" + seriesName + "|" + seriesId + "\n")
        except:
            print("Cache Error")