from enum import IntEnum

DEBUG = True

# Guild's ID
RAPAX_GUILD = 680755400655765515

# Text channels' ID
CH_TXT_TESTING = 711212263062765608
CH_TXT_CALENDARIO = 968049716132712488
CH_TXT_COM_DEL_COMANDO = 680757461606727710
CH_TXT_COM_TRA_MEMBRI = 680757657866600461
CH_TXT_PRIGIONE = 783375373285982208
CH_TXT_SALONE_OSPITI = 680765532626223215

# Voice channels' ID
CH_VCL_SALA_AMMINISTRAZIONE = 763116855660642414
CH_VCL_PLANCIA_PUBBLICA = 821000173491978272
CH_VCL_PRIGIONE_VOCALE = 836152721781293067

# Roles' ID
AMMINISTRATORE = 680772355940679689
COMANDANTE = 680766448553295919
UFFICIALE_ESECUTIVO = 680766526953095179
RECLUTATORE = 680766568531361792
UFFICIALE = 708602735100166215
MEMBRO_DEL_CLAN = 680766615234543662
CB_ALPHA = 968099514743410688
CB_BRAVO = 968099448876048424
OSPITI = 680776924859334672
PRIGIONIERO = 783375143593836595
TORPAMICI = 696828138591879189


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
    TRAINING = 1
    CLAN_BRAWL = 2
    CLAN_BATTLE = 3
    OTHER = 4


class ShipsTypeEnum(IntEnum):
    DESTROYER = 1
    CRUISER = 2
    BATTLESHIP = 3
    AIR_CARRIER = 4
    SUBMARINE = 5


class ShipsTierEnum(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11


# Some Tuples
authorizationLevel = (-1, AMMINISTRATORE, COMANDANTE, UFFICIALE_ESECUTIVO,
                      RECLUTATORE, UFFICIALE, MEMBRO_DEL_CLAN, OSPITI)

wowsEvent = ('', 'allenamento', 'Clan Brawl', 'Clan Battle', 'torneo')

shipsType = ('', 'Destroyer', 'Cruiser', 'Battleship', 'AirCarrier',
             'Submarine')

voteEmoji = ("\U00002705", "\U0000274C", "\U00002753")

voteKeys = (
    "- \U00002705 Presente",
    "- \U0000274C Assente",
    "- \U00002753 Forse"
)

weeklyCBEmoji = (":one:", ":two:", ":three:", ":four:", ":five:", ":six:",
                 ":seven:", ":eight:")

weeklyCBKeys = (
    "- :one: MER 19:00-21:00",
    "- :two: MER 21:00-23:00",
    "- :three: GIO 19:00-21:00",
    "- :four: GIO 21:00-23:00",
    "- :five: SAB 19:00-21:00",
    "- :six: SAB 21:00-23:00",
    "- :seven: DOM 19:00-21:00",
    "- :eight DOM 21:00-23:00",
)

weeklyEventEmoji = (":one:", ":two:", ":three:", ":four:", ":five:", ":six:",
                    ":seven:")

weeklyEventKeys = ("- :one: lunedì", "- :two: martedì", "- :three: mercoledì",
                   "- :four: giovedì", "- :five: venerdì", "- :six: sabato",
                   "- :seven: domenica")
