import discord
import random
from discord.ext import commands
from random import randrange
from utils import *

class Entmt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed()
        embed.colour = discord.Colour.from_rgb(152, 4, 11)
        embed.description = "Il prefisso da usare è: `>`\n `[]` indica un parametro opzionale. \n `{}` indica un parametro ripetibile."
        embed.set_author(name = "RapaxBot", icon_url = "https://cdn.discordapp.com/attachments/711212263062765608/781507702853074964/Rapax_circle.png")
        embed.add_field(name = "`CB day time {time}`", value = "Genera in *com-del-comando* un messaggio per le Clan Battle.", inline = False)
        embed.add_field(name = "`cb day time {time}`", value = "Genera in *com-del-comando* un messaggio per le Clan Brawl.", inline = False)
        embed.add_field(name = "`write channel_ID message`", value = "Scrive il *message* nel canale con ID *channel_ID*", inline = False)
        embed.add_field(name = "`edit channel_ID message_ID messagge`", value = "Sostituisce il messaggio del bot con ID *message_ID* col testo *messagge*.", inline = False)
        embed.add_field(name = "`add_emoji message_ID emoji`", value = "Aggiunge la reazione *emoji* al messaggio con ID *message_ID*.", inline = False)
        embed.add_field(name = "`vote [message_ID]`", value = "Aggiunge le reazioni al messaggio con ID *message_ID*.", inline = False)
        embed.add_field(name = "`prison @member timer reason`", value = "Aggiunge il ruolo `Prigioniero` a ``@member` per `timer` secondi.", inline = False)
        embed.add_field(name = "`torp @member`", value = "Aggiunge il ruolo `Torpamici` a `@member` per un\"ora.", inline = False)
        embed.add_field(name = "`nickname`", value = "Cambia il nickname dei membri che hanno il tag *ospiti* con il loro nickname di gioco.", inline = False)
        embed.add_field(name = "`ping`", value = "Pong!", inline = False)
        embed.add_field(name = "`dice number`", value = "Lancia un dado a `number` facce.", inline = False)
        embed.add_field(name = "`coin`", value = "Lancia una moneta.", inline = False)
        embed.set_footer(text = "Per avere l\"ID di un messaggio o canale, bisogna attivare la modalità sviluppatore su Discord." )
        await ctx.send(embed = embed)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def dice(self, ctx, number):
        number = int(number)
        await ctx.send(randrange(number) + 1)

    @commands.command()
    async def coin(self, ctx):
        moneta = ["Testa", "Croce"]
        await ctx.send(random.choice(moneta))


def setup(bot):
    bot.add_cog(Entmt(bot))
