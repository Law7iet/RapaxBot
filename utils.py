
# Costants

# Channels' ID
TESTING = 711212263062765608
COM_DEL_COMANDO = 680757461606727710
PRIGIONE = 783375373285982208

# Roles' ID
AMMINISTRATORE = 680772355940679689
COMANDANTE = 680766448553295919
UFFICIALE_ESECUTIVO = 680766526953095179
RECLUTATORE = 680766568531361792
MEMBRO_DEL_CLAN = 680766615234543662
PRIGIONIERO = 783375143593836595
TORPAMICI = 696828138591879189
OSPITI = 680776924859334672

# Tuple of reactions
votazioni = ('\U00002705', '\U0000274C', '\U00002753')
significato_votazioni = ('Si', 'No', 'Non lo so')
votazioni_cb = ('\U00002705', '\U0000274C', '\U00002753', '\U0000267B', '\U0001f559')
significato_votazioni_cb = ('Si', 'No', 'Non lo so', 'Riserva', 'Arrivo tardi')

# WoWs API
URL_PLAYER_ID = 'https://api.worldofwarships.eu/wows/account/list/?application_id=' + config.data['API'] + '&search='
URL_PLAYER_CLAN_ID = 'https://api.worldofwarships.eu/wows/clans/accountinfo/?application_id=' + config.data['API'] + '&account_id='
URL_CLAN_NAME = 'https://api.worldofwarships.eu/wows/clans/info/?application_id=' + config.data['API'] + '&clan_id='

# Support fuctions

# Check if the sender has the correct role
def check_role(ctx):
    for role in ctx.message.author.roles:
        if role.name == 'Amministratore' or role.name == 'Comandante' or role.name == 'Ufficiale esecutivo' or role.name == 'Reclutatore':
            return True
    return False

# Setup the messagge for the clan battle/brawl notification
def clan_message(flag):
    type = 'Battle.\n' if flag else 'Brawl.\n'
    message = '<@&680766615234543662>\nSegnalateci la vostra disponibilità per le Clan ' + type + 'Legenda:\n'
    for i in range(5):
        message = message + '- ' + votazioni_cb[i] + ' ' + significato_votazioni_cb[i] + '\n'
    return message

# Setup the message for the clan battle/brawl partecipation
def clan_participation(flag, day, hour):
    type = 'Battle' if flag else 'Brawl'
    message = 'Presenze delle Clan ' + type + ' di ' + day + ', ore: ' + hour
    return message

# Check if the recived data is correct
def check_data(URL):
    # send request
    reply = requests.get(url = URL)
    data = reply.json()
    # check data errors
    if data['status'] != 'ok':
        return 'Status error: ' + data['status']
    else:
        return data

# Get the player's ID from his nickname
def get_player_ID(nickname):
    # get player ID
    URL = URL_PLAYER_ID + nickname
    # check data errors
    data = check_data(URL)
    try:
        data = data['data']
        data.reverse()
        data = data.pop()
        return [data['nickname'], data['account_id']]
    except:
        return -1

# Get the player's clan's ID from his ID
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

# Get the clan's name form its ID
def get_clan_name(ID):
    # get clan name
    URL = URL_CLAN_NAME + str(ID)
    # check data errors
    data = check_data(URL)
    data = data['data']
    if data[str(ID)]['tag'] != None:
        return data[str(ID)]['tag']
