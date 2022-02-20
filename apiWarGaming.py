import config
from utils import *

class ApiWarGaming:
    def __init__(self):
        self.urlPlayers = 'https://api.worldofwarships.eu/wows/account/list/?application_id=' + config.data["APPLICATION_ID"] + '&search='
        self.urlPlayerPersonalData = 'https://api.worldofwarships.eu/wows/account/info/?application_id=' + config.data["APPLICATION_ID"] + '&account_id='
        self.urlClans = 'https://api.worldofwarships.eu/wows/clans/list/?application_id=' + config.data["APPLICATION_ID"] + '&search='
        self.urlClanDetails = 'https://api.worldofwarships.eu/wows/clans/info/?application_id=' + config.data["APPLICATION_ID"] + '&clan_id='
        self.urlPlayerClanData = 'https://api.worldofwarships.eu/wows/clans/accountinfo/?application_id=' + config.data["APPLICATION_ID"] + '&account_id='        
        self.urlClanRanking = 'https://clans.worldofwarships.eu/api/clanbase/'

    def getUrlClanRanking(self):
        return self.urlClanRanking

    # Search the first player whose nickname matches with the parameter and
    # returns its nickname and its id
    def getPlayerByNick(self, nickname):
        url = self.urlPlayers + nickname
        # api call and check if the response is ok
        response = checkData(url)
        try:
            data = response['data'][0]
            return (data['account_id'], data['nickname'])
        except:
            return None

    # Search the player's clan's id by the player's id
    def getClanByPlayerId(self, id):
        url = self.urlPlayerClanData + str(id)
        response = checkData(url)
        try:
            data = response['data']
            return (data[str(id)]['clan_id'])
        except:
            return None

    # Get the clan's name and tag by the clan's id
    def getClanNameById(self, id):
        url = self.urlClanDetails + str(id)
        response = checkData(url)
        try:
            data = response['data']
            return (data[str(id)]['name'], data[str(id)]['tag'])
        except:
            return None