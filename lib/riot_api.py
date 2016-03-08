"""
Contains the api call stuff.
Thanks to https://github.com/Kruptein, I copied much of his lolapi repo. :)
"""

import os
import json
import requests
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
# Globals
RIOT_KEY = ""
REGION_ENDPOINT = "https://{0}.api.pvp.net/api/lol/{0}/"
STATIC_DATA_ENDPOINT = "https://global.api.pvp.net/api/lol/static-data/{0}/"

def setup():
    """
    Get setup for calls, getting the api keys from the config file.
    """
    global RIOT_KEY
    with open(os.path.join(__location__, 'config'), 'r') as f:
        try:
            config = json.load(f)
        except ValueError:
            config = {"riot_key": "", "championgg_key": ""}
    RIOT_KEY = config["riot_key"]

# Riot API calls

def get_summoner_by_name(region, summonerNames):
    """
    Get summoner objects mapped by standardized summoner name
    for a given list of summoner names.
    """
    return requests.get(
        (REGION_ENDPOINT + "v1.4/summoner/by-name/{1}?&api_key={2}").
        format(region, summonerNames, RIOT_KEY))
        
def get_summoner_by_id(region, summonerIds):
    """
    Get summoner objects mapped by summoner ID
    for a given list of summoner IDs.
    """
    return requests.get(
        (REGION_ENDPOINT + "v1.4/summoner/{1}?api_key={2}").
        format(region, summonerIds, RIOT_KEY))
        

def get_runes(region, summonerIds):
    """
    Get rune pages mapped by summoner ID
    for a given list of summoner IDs.
    """
    return requests.get(
        (REGION_ENDPOINT + "v1.4/summoner/{1}/runes?api_key={2}").
        format(region, summonerIds, RIOT_KEY))
        
        
def get_champion_list(
        region="na", locale="", version="",
        dataById="", champData=""):
    """
    Retrieves list of all champions currently in the game.
    """
    return requests.get(
        (STATIC_DATA_ENDPOINT + "v1.2/champion?locale={1}&version={2}"
         "&dataById={3}&champData={4}&api_key={5}").
        format(region, locale, version, dataById, champData, RIOT_KEY))
        
# Helpers
def get_summoner_id(region, summonerName):
    """
    Get your summoner id.
    """
    if "," in summonerName:
        print("Call this one id at a time ;)")
        return
        
    return get_summoner_by_name(region, summonerName).json()[summonerName.lower()]['id']
    
def get_all_champion_names():
    """
    Helper to get a list of all the champions in the game currently, from riot's api.
    """
    champ_dict = get_champion_list(champData="all").json()['data']
    return list(champ_dict.keys())