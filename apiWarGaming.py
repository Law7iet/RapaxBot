import config
import json
from utils import *

class ApiWarGaming:
    def __init__(self):
        self.urlPlayers = 'https://api.worldofwarships.eu/wows/account/list/?application_id=' + config.data['APPLICATION_ID'] + '&search='
        self.urlPlayerPersonalData = 'https://api.worldofwarships.eu/wows/account/info/?application_id=' + config.data['APPLICATION_ID'] + '&account_id='
        self.urlClans = 'https://api.worldofwarships.eu/wows/clans/list/?application_id=' + config.data['APPLICATION_ID'] + '&search='
        self.urlClanDetails = 'https://api.worldofwarships.eu/wows/clans/info/?application_id=' + config.data['APPLICATION_ID'] + '&clan_id='
        self.urlPlayerClanData = 'https://api.worldofwarships.eu/wows/clans/accountinfo/?application_id=' + config.data['APPLICATION_ID'] + '&account_id='        
        self.urlClanRanking = 'https://clans.worldofwarships.eu/api/clanbase/'
        self.urlShips = 'https://api.worldofwarships.eu/wows/encyclopedia/ships/?application_id=' + config.data['APPLICATION_ID'] + '&fields=name%2C+tier%2C+is_special%2C+is_premium%2C+type%2C+nation&page_no='

    def getClanRanking(self, clanId: int) -> list:
        '''
        Returns the ratings of a clan.
        The ratings is divided by 'season_number'.
        Each season number has 2 istance of rating, defined by 'team_number' and it represents alpha and bravo squad.

        Args:
            `clanId` (int): the clan ID.

        Returns:
            `list`: the list of ratings.
        '''        
        url = self.urlClanRanking + str(clanId) + '/claninfo/'
        return json.loads((requests.get(url = url)).text)['clanview']['wows_ladder']['ratings']

    def getUrlShips(self) -> str:
        '''
        Returns the url for the information of World of Warhips ships.
        
        Returns:
            `str`: the url.
        '''

    def getPlayerByNick(self, nickname: str) -> tuple | None:
        '''
        Search the first player whose nickname matches with the parameter and returns its nickname and its ID.

        Args:
            `nickname` (str): the nickname.

        Returns:
            `tuple`: it contains the id and nickname. If the input nickname doesn't match with any player, it returns `None`.
        '''        
        url = self.urlPlayers + nickname
        # api call and check if the response is ok
        response = checkData(url)
        try:
            data = response['data'][0]
            return (data['account_id'], data['nickname'])
        except:
            return None

    def getClanByPlayerId(self, id: int) -> tuple | None:
        '''
        Search the player's clan's id by the player's ID.
        
        Args:
            `id` (int): the ID of the player.

        Returns:
            `tuple`: it contains the clan ID. If the player has not a clan, it returns `None`.
        '''        
        url = self.urlPlayerClanData + str(id)
        response = checkData(url)
        try:
            data = response['data']
            return (data[str(id)]['clan_id'])
        except:
            return None

    def getClanNameById(self, id: int) -> tuple | None:
        '''
        Get the clan's name and tag by the clan's ID.

        Args:
            `id` (int): the ID of the clan

        Returns:
            `tuple` | `None`: it contains the clan name and clan tag. If the ID isn't valid, it returns `None`.
        '''        
        url = self.urlClanDetails + str(id)
        response = checkData(url)
        try:
            data = response['data']
            return (data[str(id)]['name'], data[str(id)]['tag'])
        except:
            return None