import requests
from discord.utils import get
from discord.ext.commands.context import Context
from enum import IntEnum

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
UFFICIALE = 708602735100166215
MEMBRO_DEL_CLAN = 680766615234543662
PRIGIONIERO = 783375143593836595
TORPAMICI = 696828138591879189
OSPITI = 680776924859334672

authorizationLevel = [
    -1,
    AMMINISTRATORE,
    COMANDANTE,
    UFFICIALE_ESECUTIVO,
    RECLUTATORE,
    UFFICIALE,
    MEMBRO_DEL_CLAN,
    OSPITI
]

class AuthorizationLevelEnum(IntEnum):
    AMMINISTRATORE = 1
    COMANDANTE = 2
    UFFICIALE_ESECUTIVO = 3
    RECLUTATORE = 4
    UFFICIALE = 5
    MEMBRO_DEL_CLAN = 6
    OSPITI = 7

class WoWsEventEnum(IntEnum):
    TRAINING = 1,
    CLAN_BRAWL = 2,
    CLAN_BATTLE = 3,
    OTHER = 4

# RAPAX clan's ID
RAPAX_ID = 500155506

# Check if the recived data is correct
def checkData(url):
    # send request
    reply = requests.get(url = url)
    data = reply.json()
    # check data errors
    if data['status'] != 'ok':
        print('Status error: ' + data['status'])
        return None
    else:
        return data

# Check if the sender has the correct role
async def checkRole(ctx: Context, level: AuthorizationLevelEnum):
    for i in range(1, int(level) + 1):
        role = get(ctx.guild.roles, id = authorizationLevel[i])
        if role in ctx.message.author.roles:
            return True
    await ctx.message.delete()
    await ctx.send(ctx.message.author.display_name + " non hai i permessi")
    return False

voteEmoji = (
    "\U00002705", 
    "\U0000274C", 
    "\U00002753"
)