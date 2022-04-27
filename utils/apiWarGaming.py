import config
from utils.functions import *
from config import data


class ApiWarGaming:
    def __init__(self):
        self.key = data['APPLICATION_ID']
        self.url_api_root = 'https://api.worldofwarships.eu/wows/'
        self.url_players = self.url_api_root + 'account/list/?application_id=' + self.key + '&search='
        self.url_player_personal_data = self.url_api_root + 'account/info/?application_id=' + self.key + '&account_id='
        self.url_clans = self.url_api_root + 'clans/list/?application_id=' + self.key + '&search='
        self.url_clan_details = self.url_api_root + 'clans/info/?application_id=' + self.key + '&clan_id='
        self.url_ships = self.url_api_root + 'encyclopedia/ships/?application_id=' + self.key + '&fields=name%2C+tier%2C+ship_id%2C+is_special%2C+is_premium%2C+type%2C+nation&page_no='
        self.url_player_ships = self.url_api_root + 'ships/stats/?application_id=' + self.key + '&fields=ship_id&account_id='
        self.url_player_clan_data = self.url_api_root + 'clans/accountinfo/?application_id=' + self.key + '&account_id='

    def get_ships(self) -> list:
        """
        Returns a list with all World of Warships' ships.

        Returns:
            the list with all ships. If an error occurs, it returns an empty list.
        """
        ships = {}
        page = 1
        while True:
            response_ships = check_data(self.url_ships + str(page))
            if response_ships is None:
                return []

            ships.update(response_ships['data'])
            page = page + 1
            if page > response_ships['meta']['page_total']:
                break

        return ships.items()

    def get_clan_members(self, clan_id: int) -> list:
        """
        Returns the list of the player's ID of the clan's ID passed in input.

        Args:
            clan_id: the clan ID.

        Returns:
            the players' ID.
        """
        clan_members = []
        response_clan_details = check_data(self.url_clan_details + str(clan_id))
        if response_clan_details is None:
            return clan_members
        for player_id in response_clan_details['data'][str(clan_id)]['members_ids']:
            clan_members.append(player_id)
        return clan_members

    def get_player_ships(self, playerId: int) -> list:
        """
        Returns the list of the player's ships.

        Args:
            playerId: the player ID.

        Returns:
            the players' ships.
        """
        ships = []
        response_member_data = check_data(self.url_player_ships + str(playerId))
        if response_member_data is None:
            return ships
        for ship in response_member_data['data'][str(playerId)]:
            ships.append(ship['ship_id'])
        return ships

    def get_player_by_nick(self, nickname: str) -> tuple | None:
        """
        Search the first player whose nickname matches with the parameter and returns its nickname and its ID.

        Args:
            nickname: the nickname.

        Returns:
            it contains the id and nickname. If the input nickname doesn't match with any player, it returns `None`.
        """
        url = self.url_players + nickname
        # api call and check if the response is ok
        response = check_data(url)
        try:
            response_data = response['data'][0]
            return response_data['account_id'], response_data['nickname']
        except Exception as error:
            print('ApiWargaming.get_player_by_nick\n' + str(error))
            return None

    def get_player_by_id(self, player_id: str) -> tuple | None:
        """
        Search the player whose ID matches with the parameter and returns its nickname and its ID.

        Args:
            player_id: the nickname.

        Returns:
            it contains the id and nickname. If the input nickname doesn't match with any player, it returns `None`.
        """
        url = self.url_player_personal_data + player_id
        # api call and check if the response is ok
        response = check_data(url)
        try:
            response_data = response['data'][str(player_id)]
            return response_data['account_id'], response_data['nickname']
        except Exception as error:
            print('ApiWargaming.get_player_by_id\n' + str(error))
            return None

    def get_clan_by_player_id(self, clan_id: int) -> tuple | None:
        """
        Search the player's clan's id by the player's ID.

        Args:
            clan_id: the ID of the player.

        Returns:
            it contains the clan ID. If the player has not a clan, it returns `None`.
        """
        url = self.url_player_clan_data + str(clan_id)
        response = check_data(url)
        try:
            response_data = response['data']
            return response_data[str(clan_id)]['clan_id']
        except Exception as error:
            print('ApiWargaming.get_clan_by_player_id\n' + str(error))
            return None

    def get_clan_name_by_id(self, clan_id: int) -> tuple | None:
        """
        Get the clan's name and tag by the clan's ID.

        Args:
            clan_id: the ID of the clan

        Returns:
            it contains the clan name and clan tag. If the ID isn't valid, it returns `None`.
        """
        url = self.url_clan_details + str(clan_id)
        response = check_data(url)
        try:
            response_data = response['data']
            return response_data[str(clan_id)]['name'], response_data[str(clan_id)]['tag']
        except Exception as error:
            print('ApiWargaming.get_clan_name_by_id\n' + str(error))
            return None
