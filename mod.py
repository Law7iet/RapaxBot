import asyncio
import discord
import re
from discord.ext import commands
from utils import *

class Mod(commands.Cog):
    
    votazioni = ("\U00002705", "\U0000274C", "\U00002753")
    significato_votazioni = ("Si", "No", "Non lo so")
    votazioni_cb = ("\U00002705", "\U0000274C", "\U00002753", "\U0001f559")
    significato_votazioni_cb = ("Si", "No", "Non lo so", "Arrivo tardi")

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
    async def presenze(self, ctx, type, input):
        if not(await self.check_role(ctx)):
            return None
        channel = self.bot.get_channel(COM_DEL_COMANDO)
        channel = self.bot.get_channel(TESTING)
        message = "<@&" + str(OSPITI) + ">"
        await channel.send(message)

        day = input.pop(0).lstrip()
        print(input)
        for hour in input:
            embed = discord.Embed()
            embed.title = type
            embed.description = "Ore " + hour.lstrip()
            embed.colour = discord.Colour.from_rgb(152, 4, 11)
            embed.set_author(name = day, icon_url = "https://cdn.discordapp.com/attachments/711212263062765608/781507702853074964/Rapax_circle.png")
            embed.add_field(name = "Presente :white_check_mark:", value = "Nessuno", inline = True)
            embed.add_field(name = "Assente :x:", value = "Nessuno", inline = True)
            embed.add_field(name = "Forse :question:", value="Nessuno", inline = True)
            embed.add_field(name = "Ritardo :clock830:", value = "Nessuno", inline = True)
            msg = await ctx.send(embed = embed)
            for element in self.votazioni_cb:
                await msg.add_reaction(element)

    @commands.command()
    async def event(self, ctx, *args):
        input = " ".join(args).split(",")
        activity = input.pop(0)
        await self.presenze(ctx, activity, input)

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
            channel_text_prison = guild.get_channel(PRIGIONE_TESTUALE)
            channel_voice_prison = guild.get_channel(PRIGIONE_VOCALE)
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
        channel = guild.get_channel(PRIGIONE_TESTUALE)
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
        print("ciao")
#        reaction.message.embed[0].

def setup(bot):
    bot.add_cog(Mod(bot))