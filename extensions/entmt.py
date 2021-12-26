import random
from random import randrange

import discord
from discord.ext import commands

from utils import *


class Entmt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
