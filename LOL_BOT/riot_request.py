import requests
import json
import os
from emblems import emojis as emblem_id
from champions import champion_by_id as champion_id

class Summoner:
    def __init__(self, tier, rank, points, wins, losses):
        self.tier = tier
        self.rank = rank
        self.points = points
        self.wins = wins
        self.losses = losses

    def win_rate(self):
        return round(((self.wins / (self.wins+self.losses)) * 100),2)

def get_ranked_data(region, api_key, summoner_id):

    URL = ('https://'+ region +'.api.riotgames.com/lol/league/v4/entries/by-summoner/'
    + summoner_id + '?api_key=' + api_key)

    response = requests.get(URL)
    response = response.json()

    if len(response) > 0:
        tier = response[0]['tier']
        rank = response[0]['rank']
        points = response[0]['leaguePoints']
        wins = response[0]['wins']
        losses = response[0]['losses']
        summ = Summoner(tier, rank, points, wins, losses)
    else:
        summ = Summoner('UNRANKED', None, None, 0, 0)

    return summ

def rank_data(region, api_key, name):

    URL = ('https://'+ region +'.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name + '?api_key=' + api_key)

    response = requests.get(URL)
    response = response.json()

    if 'id' in response:
        ID = str(response['id'])
    else:
        return str("Summoner doesn't exist on the " + region + " server.")

    SummonerData = get_ranked_data(region, api_key, ID)

    if SummonerData.tier == 'UNRANKED':
        output = str(name + " is UNRANKED") 
    else:
        output = str(name + " has\n" + emblem_id[SummonerData.tier]
        + " " + SummonerData.tier + " " + SummonerData.rank 
        + " " + str(SummonerData.points) + " LP\n\nSummoner has played "
        + str(SummonerData.wins + SummonerData.losses) + " games.\nWin rate: "
        + str(SummonerData.win_rate()) + "%" )

    return output

def free_champions(api_key, region):

    URL = ('https://' + region 
    + '.api.riotgames.com/lol/platform/v3/champion-rotations?api_key=' + api_key)

    response = requests.get(URL)
    response = response.json()

    free_champions_list = []

    for champ_id in response['freeChampionIds']:
        free_champions_list.append(champion_id[champ_id])

    output = "\n".join(free_champions_list)
    return output
