import requests
import json

URL_PLAYER_ID = 'https://api.worldofwarships.eu/wows/account/list/?application_id=9ce03c66a05fe16e0760cf5f4e11c02e&search='
URL_PLAYER_CLAN_ID = 'https://api.worldofwarships.eu/wows/clans/accountinfo/?application_id=9ce03c66a05fe16e0760cf5f4e11c02e&account_id='
URL_CLAN_NAME = 'https://api.worldofwarships.eu/wows/clans/info/?application_id=9ce03c66a05fe16e0760cf5f4e11c02e&clan_id='

def check_data(URL):
    # send request
    reply = requests.get(url = URL)
    data = reply.json()
    # check data errors
    if data['status'] != 'ok':
        return 'Status error: ' + data['status']
    else:
        return data

def get_player_ID(nickname):
    # get player ID
    URL = URL_PLAYER_ID + nickname
    # check data errors
    data = check_data(URL)
    if data['meta']['count'] == 0:
        return -1
    else:
        data = data['data']
        data.reverse()
        data = data.pop()
        return [data['nickname'], data['account_id']]

def get_clan_ID(ID):
    # get clan ID
    URL = URL_PLAYER_CLAN_ID + str(ID)
    # check data errors
    data = check_data(URL)
    data = data['data']
    if data[str(ID)]['clan_id'] == None:
        return -1
    else:
        return data[str(ID)]['clan_id']

def get_clan_name(ID):
    # get clan name
    URL = URL_CLAN_NAME + str(ID)
    # check data errors
    data = check_data(URL)
    data = data['data']
    if data[str(ID)]['tag'] == None:
        print('Tag vuoto')
    else:
        return data[str(ID)]['tag']
