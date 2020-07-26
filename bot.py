import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '>')

testingID = 711212263062765608

@bot.event
async def on_ready():
    channel = bot.get_channel(testingID)
    message = 'RapaxBot è pronto a salpare!'
    await channel.send(message)

bot.run('NzEwOTAzMTI0NzI2MTIwNTA4.Xr7ONw.H1O1R6aLaOWZaUNgfvqdt9ptBOk')
