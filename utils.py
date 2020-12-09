import discord
from discord.ext import commands

# Bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '>', intents = intents)
bot.remove_command('help')

# Secret token
TOKEN = 'NzEwOTAzMTI0NzI2MTIwNTA4.Xr7ONw.H1O1R6aLaOWZaUNgfvqdt9ptBOk'

# Channels' ID
testing_ID = 711212263062765608
comando_ID = 680757461606727710
prigione_ID = 783375373285982208

# Roles' ID
amministratore_ID = 680772355940679689
comandante_ID = 680766448553295919
ufficiale_esecutivo_ID = 680766526953095179
recludatore_ID = 680766568531361792
membro_del_clan_ID = 680766615234543662
prigionero_ID = 783375143593836595

# Tuple of reactions
votazioni = ('\U00002705', '\U0000274C', '\U00002753')
significato_votazioni = ('Si', 'No', 'Non lo so')
votazioni_cb = ('\U00002705', '\U0000274C', '\U00002753', '\U0000267B', '\U0001f559')
significato_votazioni_cb = ('Si', 'No', 'Non lo so', 'Riserva', 'Arrivo tardi')
