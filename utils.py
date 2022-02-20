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

# Guild's ID
RAPAX_GUILD = 680755400655765515

# Some Enums
class AuthorizationLevelEnum(IntEnum):
    AMMINISTRATORE = 1
    COMANDANTE = 2
    UFFICIALE_ESECUTIVO = 3
    RECLUTATORE = 4
    UFFICIALE = 5
    MEMBRO_DEL_CLAN = 6
    OSPITI = 7


class WowsEventEnum(IntEnum):
    TRAINING = 1,
    CLAN_BRAWL = 2,
    CLAN_BATTLE = 3,
    OTHER = 4


# Some Tuples
authorizationLevel = (
    -1,
    AMMINISTRATORE,
    COMANDANTE,
    UFFICIALE_ESECUTIVO,
    RECLUTATORE,
    UFFICIALE,
    MEMBRO_DEL_CLAN,
    OSPITI
)

wowsEvent = (
    '',
    'allenamento',
    'Clan Brawl',
    'Clan Battle',
    'torneo'
)

voteEmoji = (
    "\U00002705",
    "\U0000274C",
    "\U00002753"
)

voteKeys = (
    "- \U00002705 Presente",
    "- \U0000274C Assente",
    "- \U00002753 Forse"
)

CBEmoji = (
    "\U00000031\U000020E3",
    "\U00000032\U000020E3",
    "\U0001F557", 
    "\U0000274C",
    "\U00002753"
)

CBKeys = (
    "- \U00000031\U000020E3 19:00-21:00", 
    "- \U00000032\U000020E3 21:00-23:00", 
    "- \U0001F557 Arrivo tardi", 
    "- \U0000274C Non disponibile", 
    "- \U00002753 Forse"
)

eventEmoji = (
    "\U00002705",
    "\U0001F557", 
    "\U0000274C",
    "\U00002753"
)

eventKeys = (
    "- \U00002705 Presente",
    "- \U0001F557 Arrivo tardi", 
    "- \U0000274C Assente",
    "- \U00002753 Forse"
)

# Some Functions
def checkData(url: str) -> dict | None:
    """
    Make an HTTP get request and check if the response is correct, checking the attribute 'status'

    Args:
        `url` (str): the url request.

    Returns:
        `response`: the url response. If the request is invalid, it return None.
    """
    # send request
    reply = requests.get(url=url)
    data = reply.json()
    # check data errors
    if data['status'] != 'ok':
        print('Status error: ' + data['status'])
        return None
    else:
        return data

async def checkRole(ctx: Context, level: AuthorizationLevelEnum) -> bool:
    """
    Check if the sender has the correct role.
    It's use for authotization member to trigger bot's command.

    Args:
        `ctx` (Context): it's the context.
        `level` (AuthorizationLevelEnum): it's the level of authorization.

    Returns:
        `hasRole`: it represents if the member has the authorization.
    """    
    for i in range(1, int(level) + 1):
        role = get(ctx.guild.roles, id = authorizationLevel[i])
        if role in ctx.message.author.roles:
            return True
    await ctx.message.delete()
    await ctx.send(ctx.message.author.display_name + " non hai i permessi")
    return False
