from tabnanny import check
import config
import requests

# Channels' ID
CH_TXT_TESTING = 711212263062765608
CH_TXT_COM_DEL_COMANDO = 680757461606727710
CH_TXT_PRIGIONE = 783375373285982208
CH_VCL_PRIGIONE_VOCALE = 836152721781293067
CH_TXT_SALONE_OSPITI = 680765532626223215
CH_TXT_COM_TRA_MEMBRI = 680757657866600461
CH_VCL_SALA_AMMINISTRAZIONE = 763116855660642414
CH_VCL_PLANCIA_PUBBLICA = 821000173491978272

# Roles' ID
AMMINISTRATORE = 680772355940679689
COMANDANTE = 680766448553295919
UFFICIALE_ESECUTIVO = 680766526953095179
RECLUTATORE = 680766568531361792
MEMBRO_DEL_CLAN = 680766615234543662
PRIGIONIERO = 783375143593836595
TORPAMICI = 696828138591879189
OSPITI = 680776924859334672

# WoWs API
URL_PLAYER_ID = "https://api.worldofwarships.eu/wows/account/list/?application_id=" + config.data["API"] + "&search="
URL_PLAYER_CLAN_ID = "https://api.worldofwarships.eu/wows/clans/accountinfo/?application_id=" + config.data["API"] + "&account_id="
URL_CLAN_NAME = "https://api.worldofwarships.eu/wows/clans/info/?application_id=" + config.data["API"] + "&clan_id="
URL_CLAN_SEARCH = "https://api.worldofwarships.eu/wows/clans/info/?application_id=" + config.data["API"] + "&search="
URL_PLAYER_SHIPS = "https://api.worldofwarships.eu/wows/ships/stats/?application_id=" + config.data["API"] + "&fields=ship_id&account_id="
URL_SHIPS = "https://api.worldofwarships.eu/wows/encyclopedia/ships/?application_id=" + config.data["API"] + "&fields=name%2C+tier%2C+is_special%2C+is_premium%2C+type%2C+nation&page_no="
URL_PLAYER_NICKNAME = "https://api.worldofwarships.eu/wows/account/info/?application_id=" + config.data["API"] + "&fields=nickname&account_id="

# RAPAX clan's ID
RAPAX_ID = 500155506

# Support fuctions

# Check if the recived data is correct
def check_data(URL):
    # send request
    reply = requests.get(url = URL)
    data = reply.json()
    # check data errors
    if data["status"] != "ok":
        return "Status error: " + data["status"]
    else:
        return data

# Get the player's ID from his nickname
def get_player_ID(nickname):
    # get player ID
    URL = URL_PLAYER_ID + nickname
    # check data errors
    data = check_data(URL)
    try:
        data = data["data"]
        data.reverse()
        data = data.pop()
        return (data["account_id"], data["nickname"])
    except:
        return (-1, -1)

# Get the player's clan's ID from his ID
def get_player_clan(ID):
    # get clan ID
    URL = URL_PLAYER_CLAN_ID + str(ID)
    # check data errors
    data = check_data(URL)
    try:
        data = data["data"]
        return data[str(ID)]["clan_id"]
    except:
        return -1
        

# Get the clan's name from its ID
def get_clan_name_by_ID(ID):
    # get clan name
    URL = URL_CLAN_NAME + str(ID)
    # check data errors
    data = check_data(URL)
    try:
        data = data["data"]
        return (data[str(ID)]["name"], data[str(ID)]["tag"])
    except:
        return -1

def get_clan_name(filter):
    URL = URL_CLAN_SEARCH + filter
    data = check_data(URL)
    try:
        data = data["data"]
        return (data[0]["name"], data[0]["tag"])
    except:
        return -1