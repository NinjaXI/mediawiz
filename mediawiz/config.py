'''
Created on 10 Dec 2018

@author: NinjaXI
'''

import re
import tomllib
from mediasources.tvdbsource import TvdbSource
from mediasources.omdbsource import OmdbSource

with open("properties.toml", "rb") as properties_file:
    properties = tomllib.load(properties_file)

seriesFormat = "%(st)s - %(sn)sx%(en)s - %(et)s" # TODO configurable
movieFormat = "%(mt)s" # TODO configurable
movieFolderFormat = "%(mt)s (%(my)s)" # TODO configurable
movieInFolder = True
seasonEpRegex = re.compile(r"([sS]\d+[eE]\d+-\d+)|([sS]\d+[eE]\d+_\d+)|([sS]\d+[eE]\d+[eE]\d+)|([sS]\d+[eE]\d+)|(\d+x\d+)")
animeEpRegex = re.compile(r" - (\d+)")
movieRegex = re.compile(r"((\d{4}.|\(\d{4}\).|)(1080p|720p|EXTENDED|HC|HDRip|DVDRip|WEB-DL))|(\(\d*\)\.\w*$)|(\.\w*$)") #TODO update regex to handle MovieName (movieYear).ext
seriesSource = TvdbSource(properties["thetvdbApiKey"])
movieSource = OmdbSource(properties["omdbApiKey"])