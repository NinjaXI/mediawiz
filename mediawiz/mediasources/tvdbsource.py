'''
Created on 21 Oct 2018

@author: NinjaXI
'''

import requests
from mediasources.basemediasource import BaseMediaSource

class TvdbSource(BaseMediaSource):
    def __init__(self, apiKey):
        self.apiurl = "https://api4.thetvdb.com/v4"

        r = requests.post(self.apiurl + "/login", json = {"apikey": apiKey}, headers = {"Content-Type": "application/json", "Accept": "application/json"})
        
        if r.status_code == 200:
            self.jwttoken = r.json()["data"]["token"]
            self.headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": "Bearer " + self.jwttoken}
        else:
            raise BaseException()


    def findSeries(self, seriesName):
        retList = []

        r = requests.get(self.apiurl + "/search", params = {"query": seriesName, "type": "series"}, headers = self.headers)

        if r.status_code == 200:
            responseJson = r.json()["data"]
            for i in responseJson:
                if "translations" in i and "eng" in i["translations"]:
                    retList.append([i["tvdb_id"], i["translations"]["eng"]])
                else:
                    retList.append([i["tvdb_id"], i["name"]])
            return retList
        else:
            raise BaseException()

    def findEpisode(self, seasonNo, episodeNo, seriesId):
        r = requests.get(self.apiurl + "/series/" + str(seriesId) + "/episodes/default", params = {"season": seasonNo, "episodeNumber": episodeNo, "page": 0}, headers = self.headers)

        if r.status_code == 200:
            responseJson = r.json()["data"]
            if responseJson["series"]["originalLanguage"] != "eng" and "eng" in responseJson["episodes"][0]["nameTranslations"]:
                return self.findEpisodeTranslation(responseJson["episodes"][0]["id"])
            else:
                return responseJson["episodes"][0]["name"]
        else:
            raise BaseException()

    def findEpisodeForAbsoluteNo(self, absoluteEpisodeNo, seriesId):
        pageNo = 0

        while True:
            r = requests.get(self.apiurl + "/series/" + str(seriesId) + "/episodes/default", params = {"page": pageNo}, headers = self.headers)

            if r.status_code == 200:
                fullResponse = r.json()
                responseJson = fullResponse["data"]

                for ep in responseJson["episodes"]:
                    if ep["absoluteNumber"] == absoluteEpisodeNo:
                        if responseJson["series"]["originalLanguage"] != "eng" and "eng" in ep["nameTranslations"]:
                            return ep["seasonNumber"], ep["number"], self.findEpisodeTranslation(ep["id"])
                        else:
                            return ep["seasonNumber"], ep["number"], ep["name"]

                if fullResponse["links"]["next"] is not None:
                    pageNo += 1
                else:
                    raise BaseException()
            else:
                raise BaseException()

    def findEpisodeTranslation(self, episodeId):
        r = requests.get(self.apiurl + "/episodes/" + str(episodeId) + "/translations/eng", headers = self.headers)

        if r.status_code == 200:
            responseJson = r.json()["data"]
            return responseJson["name"]
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