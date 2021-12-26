import asyncio
import re

import discord
from discord.ext import commands

from utils import *


class Mod(commands.Cog):
    
    votazioni = ("\U00002705", "\U0000274C", "\U00002753")
    votazioni_cb = ("\U00000031\U000020E3", "\U00000032\U000020E3", "\U0001F557", "\U0000274C", "\U00002753")
    fields = ("- \U00000031\U000020E3 19:00-21:00", "- \U00000032\U000020E3 21:00-23:00", "- \U0001F557 Con ritardo", "- \U0000274C Non disponibile", "- \U00002753 Forse")

    def __init__(self, bot):
        self.bot = bot
    
    # Check if the sender has the correct role
    async def check_role(self, ctx):
        for role in ctx.message.author.roles:
            if role.id == AMMINISTRATORE or role.id == COMANDANTE or role.id == UFFICIALE_ESECUTIVO or role.id == RECLUTATORE:
                return True
        await ctx.message.delete()
        await ctx.send(ctx.message.author.display_name + " non hai i permessi")
        return False

    # Generate the partecipation message for Clan Battles or Clan Brawl
    async def presenze(self, ctx, type, day):
        if not(await self.check_role(ctx)):
            return None

        channel = self.bot.get_channel(CH_TXT_COM_DEL_COMANDO)
        message = "<@&" + str(MEMBRO_DEL_CLAN) + ">"
        # TEST MODE
        # channel = self.bot.get_channel(CH_TXT_TESTING)
        # message = "<@&" + str(OSPITI) + ">"

        await channel.send(message)

        # DAYLY EMBED
        embed=discord.Embed(title="Presenze Clan Battle", description=day + "\n\n" + "\n".join(self.fields), color=0xffd519)
        embed.set_author(name="RapaxBot")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/675275973918195712/924566156407341076/Logo_RAPAX_Cerchio.png")

        # WEEKLY EMBED
        # embed=discord.Embed(title="Presenze Clan Battle", description="Settimana dal 20/12 al 26/12", color=0xffd519)
        # embed.set_author(name="RapaxBot")
        # embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/675275973918195712/924566156407341076/Logo_RAPAX_Cerchio.png")
        # embed.add_field(name="Mercoledì", value=":one: 19:00-20:30 \n :two: 21:00-23:00 ", inline=False)
        # embed.add_field(name="Giovedì", value=":three: 19:00-20:30 \n :four: 21:00-23:00 ", inline=False)
        # embed.add_field(name="Sabato", value=":five: 19:00-20:30 \n :six: 21:00-23:00 ", inline=False)
        # embed.add_field(name="Domenica", value=":seven: 19:00-20:30 \n :eight: 21:00-23:00 ", inline=False)
        # await ctx.send(embed=embed)

        msg = await ctx.send(embed = embed)
        for element in self.votazioni_cb:
            await msg.add_reaction(element)

    @commands.command()
    async def write(self, ctx, channel_id, *message):
        if not(await self.check_role(ctx)):
            return None
        guild = ctx.guild
        channel = guild.get_channel(int(channel_id))
        text = ""
        for word in message:
            text = text + " " + word
        await channel.send(text)

    @commands.command()
    async def edit(self, ctx, channel_id, message_id, *new_message):
        if not(await self.check_role(ctx)):
            return None
        guild = ctx.guild
        channel = guild.get_channel(int(channel_id))
        message = await channel.fetch_message(int(message_id))
        text = ""
        for word in new_message:
            text = text + " " + word
        await message.edit(content = text)

    # It works only for deafult's emoji and server's emoji
    @commands.command()
    async def add_emoji(self, ctx, message_id, emoji):
        if not(await self.check_role(ctx)):
            return None
        channel = ctx.message.channel
        await ctx.message.delete()
        message = await channel.fetch_message(int(message_id))
        await message.add_reaction(emoji)

    @commands.command()
    async def vote(self, ctx, message_id):
        channel = ctx.message.channel
        author = ctx.message.author
        msg = await channel.fetch_message(int(message_id))
        if msg.author != author:
            if not(await self.check_role(ctx)):
                return None
        await ctx.message.delete()
        for element in self.votazioni:
            await msg.add_reaction(element)
    
    @commands.command()
    async def CB(self, ctx, day):
        await self.presenze(ctx, "Clan Battle", day)
    
    @commands.command()
    async def cb(self, ctx, day):
        await self.presenze(ctx, "Clan Brawl", day)

    @commands.command()
    async def nickname(self, ctx):
        if not(await self.check_role(ctx)):
            return None
        guild = ctx.guild
        members = guild.members
        for member in members:
            if guild.get_role(OSPITI) in member.roles:
                user = member.display_name
                user = re.sub(r"\[.+\]", "", user)
                user = user.lstrip()
                name = re.search(r"\(([A-Za-z0-9_]+)\)", user)
                if name != None:
                    user = re.sub(r"\(.+\)", "", user)
                    name = name.group(1)
                player_info = get_player_ID(user)
                try:
                    game_nick = player_info[0]
                    player_id = player_info[1]
                    clan_id = get_clan_ID(player_id)
                    new_nick = game_nick
                    if clan_id != -1:
                        clan_tag = get_clan_name(clan_id)
                        new_nick = "[" + clan_tag + "] " + game_nick
                    if name != None and len(new_nick + " (" + name + ")") <= 32:
                        new_nick = new_nick + " (" + name + ")"
                    await member.edit(nick=new_nick)
                except:
                    await ctx.send("Il membro `" + user + "` non è stato trovato.")
    
    @commands.command()
    async def prison(self, ctx, member: discord.Member, time, *message):
        if not(await self.check_role(ctx)):
            return None
        if time.isnumeric():
            guild = ctx.guild
            channel_text_prison = guild.get_channel(CH_TXT_PRIGIONE)
            channel_voice_prison = guild.get_channel(CH_VCL_PRIGIONE_VOCALE)
            role = guild.get_role(AMMINISTRATORE)
            list_roles = member.roles
            if role in list_roles:
                list_roles.remove(role)
            role = guild.get_role(PRIGIONIERO)
            flag = True
            if role in list_roles:
                await ctx.send("È già prigionero")
                flag = False
            if flag == True:
                for i in range(1, len(list_roles)):
                    await member.remove_roles(list_roles[i])
                await member.add_roles(role)
                try:
                    member.voice.channel != None
                    channel_voice = member.voice.channel
                    await member.move_to(channel_voice_prison)
                except:
                    pass
                text = ""
                for word in message:
                    text = text + " " + word
                message = member.display_name + " è stato messo in prigione per " + time + " secondi.\nMotivazione:" + text
                await channel_text_prison.send(message)
                timer = int(time)
                while True:
                    timer -= 1
                    if timer == 0:
                        await channel_text_prison.send(member.display_name + " ha scontato la propria pena. Fine della quarantena.")
                        break
                    await asyncio.sleep(1)
                for i in range(1, len(list_roles)):
                    await member.add_roles(list_roles[i])
                await member.remove_roles(role)
                try:
                    await member.move_to(channel_voice)
                except:
                    pass
        else:
            await ctx.send(ctx.author.display_name + " hai inserito degli argomenti errati")

    @commands.command()
    async def torp(self, ctx, member: discord.Member):
        if not(await self.check_role(ctx)):
            return None
        guild = ctx.guild
        channel = guild.get_channel(CH_TXT_PRIGIONE)
        role = guild.get_role(TORPAMICI)
        list_roles = member.roles
        flag = True
        if role in list_roles:
            await ctx.send("È già un torpamico")
            flag = False
        if flag:
            await member.add_roles(role)
            message = member.name + " è diventato un torpamico per un\'ora."
            await channel.send(message)
            await asyncio.sleep(3600)
            await channel.send(member.name + " non è più torpamico.")
            await member.remove_roles(role)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        nickname = user.display_name

def setup(bot):
    bot.add_cog(Mod(bot))
