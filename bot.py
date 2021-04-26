from random import randrange
import random
import discord
from discord.ext import commands
import asyncio
import config
import re
from utils import *

# Bot"s setup
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = config.data["PREFIX"], intents = intents)
bot.remove_command("help")

# Bot"s events
#@bot.event
#async def on_ready():
#    channel = bot.get_channel(TESTING)
#    message = "RapaxBot è pronto a salpare!"
#    await channel.send(message)

# Bot"s commands
@bot.command()
async def help(ctx):
    embed = discord.Embed()
    embed.colour = discord.Colour.from_rgb(152, 4, 11)
    embed.description = "Il prefisso da usare è: `>`\n `[]` indica un parametro opzionale. \n `{}` indica un parametro ripetibile."
    embed.set_author(name = "RapaxBot", icon_url = "https://cdn.discordapp.com/attachments/711212263062765608/781507702853074964/Rapax_circle.png")
    embed.add_field(name = "`CB day time {time}`", value = "Genera in *com-del-comando* un messaggio per le Clan Battle.", inline = False)
    embed.add_field(name = "`cb day time {time}`", value = "Genera in *com-del-comando* un messaggio per le Clan Brawl.", inline = False)
    embed.add_field(name = "`write channel_ID message`", value = "Scrive il *message* nel canale con ID *channel_ID*", inline = False)
    embed.add_field(name = "`edit channel_ID message_ID messagge`", value = "Sostituisce il messaggio con ID *message_ID* col testo *messagge*.", inline = False)
    embed.add_field(name = "`add_emoji message_ID emoji`", value = "Aggiunge la reazione *emoji* al messaggio con ID *message_ID*.", inline = False)
    embed.add_field(name = "`vote [message_ID]`", value = "Aggiunge le reazioni per votare all\"ultimo messaggio inviato dall\"autore, o al messaggio con ID *message_ID*.", inline = False)
    embed.add_field(name = "`prison @member timer reason`", value = "Aggiunge il ruolo `Prigioniero` a ``@member` per `timer` secondi.", inline = False)
    embed.add_field(name = "`torp @member`", value = "Aggiunge il ruolo `Torpamici` a `@member` per un\"ora.", inline = False)
    embed.add_field(name = "`nickname`", value = "Cambia il nickname dei membri che hanno il tag *ospiti* con il loro nickname di gioco.", inline = False)
    embed.add_field(name = "`dice number`", value = "Lancia un dado a `number` facce.", inline = False)
    embed.add_field(name = "`coin`", value = "Lancia una moneta.", inline = False)
    embed.set_footer(text = "Per avere l\"ID di un messaggio o canale, bisogna attivare la modalità sviluppatore su Discord." )
    await ctx.send(embed = embed)

@bot.command()
async def CB(ctx, *args):
    flag = check_role(ctx)
    if flag == True:
        channel = bot.get_channel(COM_DEL_COMANDO)
        i = 1
        message = clan_message(1)
        await channel.send(message)
        while i < len(args):
                message = clan_participation(1, args[0], args[i])
                msg = await channel.send(message)
                for element in votazioni_cb:
                    await msg.add_reaction(element)
                i = i + 1
    else:
        await ctx.message.delete()
        await ctx.send("Non hai i permessi")

@bot.command()
async def cb(ctx, *args):
    flag = check_role(ctx)
    if flag == True:
        channel = bot.get_channel(COM_DEL_COMANDO)
        i = 1
        message = clan_message(0)
        await channel.send(message)
        while i < len(args):
                message = clan_participation(0, args[0], args[i])
                msg = await channel.send(message)
                for element in votazioni_cb:
                    await msg.add_reaction(element)
                i = i + 1
    else:
        await ctx.message.delete()
        await ctx.send("Non hai i permessi")

@bot.command()
async def write(ctx, channel_id, *message):
    flag = check_role(ctx)
    if flag == True:
        guild = ctx.guild
        channel = guild.get_channel(int(channel_id))
        text = ""
        for word in message:
            text = text + " " + word
        await channel.send(text)
    else:
        await ctx.message.delete()
        await ctx.send("Non hai i permessi")

@bot.command()
async def edit(ctx, channel_id, message_id, *new_message):
    flag = check_role(ctx)
    if flag == True:
        guild = ctx.guild
        channel = guild.get_channel(int(channel_id))
        message = await channel.fetch_message(int(message_id))
        text = ""
        for word in new_message:
            text = text + " " + word
        await message.edit(content = text)
    else:
        await ctx.message.delete()
        await ctx.send("Non hai i permessi")

# It works only for deafult"s emoji and server"s emoji
@bot.command()
async def add_emoji(ctx, message_id, emoji):
    flag = check_role(ctx)
    if flag == True:
        channel = ctx.message.channel
        await ctx.message.delete()
        message = await channel.fetch_message(int(message_id))
        await message.add_reaction(emoji)
    else:
        await ctx.message.delete()
        await ctx.send("Non hai i permessi")

@bot.command()
async def vote(ctx, *args):
    if len(args) == 0:
        await ctx.message.delete()
        author = ctx.message.author
        channel = ctx.message.channel
        msg = await channel.history().get(author = author)
        for element in votazioni:
            await msg.add_reaction(element)
    else:
        flag = check_role(ctx)
        if flag == True:
            await ctx.message.delete()
            message_id = args[0]
            channel = ctx.message.channel
            msg = await channel.fetch_message(int(message_id))
            for element in votazioni:
                await msg.add_reaction(element)
        else:
            await ctx.message.delete()
            await ctx.send("Non hai i permessi")

@bot.command()
async def dice(ctx, number):
    number = int(number)
    await ctx.send(randrange(number) + 1)

@bot.command()
async def coin(ctx):
    moneta = ["Testa", "Croce"]
    await ctx.send(random.choice(moneta))

@bot.command()
async def prison(ctx, member: discord.Member, time, *message):
    flag = check_role(ctx)
    if flag == True:
        if time.isnumeric():
            guild = ctx.guild
            channel_text_prison = guild.get_channel(PRIGIONE_TESTUALE)
            channel_voice_prison = guild.get_channel(PRIGIONE_VOCALE)
            role = guild.get_role(AMMINISTRATORE)
            list_roles = member.roles
            if role in list_roles:
                list_roles.remove(role)
            role = guild.get_role(PRIGIONIERO)
            if role in list_roles:
                await ctx.send("È già prigionero")
                flag = False
            if flag == True:
                for i in range(1, len(list_roles)):
                    await member.remove_roles(list_roles[i])
                await member.add_roles(role)
                if member.voice.channel != None:
                    channel_voice = member.voice.channel
                    await member.move_to(channel_voice_prison)
                text = ""
                for word in message:
                    text = text + " " + word
                message = member.name + " è stato messo in prigione per " + time + " secondi.\nMotivazione:" + text
                await channel_text_prison.send(message)
                timer = int(time)
                while True:
                    timer -= 1
                    if timer == 0:
                        await channel_text_prison.send(member.name + " ha scontato la propria pena. Fine della quarantena.")
                        break
                    await asyncio.sleep(1)
                for i in range(1, len(list_roles)):
                    await member.add_roles(list_roles[i])
                await member.remove_roles(role)
                if member.voice.channel != None:
                    await member.move_to(channel_voice)
        else:
            await ctx.send(ctx.author.nick + " hai inserito degli argomenti errati")
    else:
        await ctx.message.delete()
        await ctx.send(ctx.author.nick + " non hai i permessi")

@bot.command()
async def torp(ctx, member: discord.Member):
    flag = check_role(ctx)
    if flag == True:
        guild = ctx.guild
        channel = guild.get_channel(PRIGIONE_TESTUALE)
        role = guild.get_role(TORPAMICI)
        list_roles = member.roles
        if role in list_roles:
                await ctx.send("È già un torpamico")
                flag = False
        if flag == True:
            await member.add_roles(role)
            message = member.name + " è diventato un torpamico per un\"ora."
            await channel.send(message)
            await asyncio.sleep(3600)
            await channel.send(member.name + " non è più torpamico.")
            await member.remove_roles(role)
    else:
        await ctx.message.delete()
        await ctx.send("Non hai i permessi")

@bot.command()
async def nickname(ctx):
    flag = check_role(ctx)
    if flag == True:
        # get all the server"s members
        guild = ctx.guild
        members = guild.members
        for member in members:
            # select only guest
            if guild.get_role(OSPITI) in member.roles:
                # select their nickname or their name if they don"t have a nickname
                if member.nick != None:
                    user = member.nick
                else:
                    user = member.name
                # delete clan tag and their real name
                user = re.sub(r"\[.+\]", "", user)
                user = user.lstrip()
                name = re.search(r"\(([A-Za-z0-9_]+)\)", user)
                if name != None:
                    user = re.sub(r"\(.+\)", "", user)
                    name = name.group(1)
                # get user"s nickname and his"s clan tag using WoWs API
                player_info = get_player_ID(user)
                try:
                    game_nick = player_info[0]
                    player_id = player_info[1]
                    clan_id = get_clan_ID(player_id)
                    # select user"s nickname
                    new_nick = game_nick
                    if clan_id != -1:
                        # add his clan"s tag
                        clan_tag = get_clan_name(clan_id)
                        new_nick = "[" + clan_tag + "] " + game_nick
                    if name != None and len(new_nick + " (" + name + ")") <= 32:
                        # add his name
                        new_nick = new_nick + " (" + name + ")"
                    # change nickname
                    await member.edit(nick=new_nick)
                except:
                    await ctx.send("Il membro `" + user + "` non è stato trovato.")

# Run bot
bot.run(config.data["TOKEN"])
