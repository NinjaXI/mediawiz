'''
Created on 21 Oct 2018

@author: NinjaXI
'''

import requests
from tvsources.basetvsource import BaseTvSource

class TvdbSource(BaseTvSource):
    def __init__(self):
        self.apiurl = "https://api.thetvdb.com/"
        
        r = requests.post(self.apiurl + "login", json = {"apikey":"BO3YJVOHA8115LB4"}, headers = {"Content-Type":"application/json", "Accept":"application/json"})
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