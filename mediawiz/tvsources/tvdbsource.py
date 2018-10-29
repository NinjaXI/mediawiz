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
        r = requests.get(self.apiurl + "search/series", params = {"name":seriesName}, headers = self.headers)
        
        if r.status_code == 200:
            retList = []
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