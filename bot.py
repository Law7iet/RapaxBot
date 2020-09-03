import random
import discord
from discord.ext import commands

TOKEN = 'NzEwOTAzMTI0NzI2MTIwNTA4.Xr7ONw.H1O1R6aLaOWZaUNgfvqdt9ptBOk'

bot = commands.Bot(command_prefix = '>')
bot.remove_command('help')

testingID = 711212263062765608
comandoID = 680757461606727710

@bot.event
async def on_ready():
    channel = bot.get_channel(testingID)
    message = 'RapaxBot è pronto a salpare!'
    await channel.send(message)

@bot.command()
async def help(ctx):

    embed = discord.Embed()
    embed.title = 'RapaxBot'
    embed.colour = discord.Colour.from_rgb(29, 228, 74)
    embed.description = 'Il prefisso da usare è: `>`'
    embed.add_field(name = '`CB giorno orario1 orario2...`', value = 'Genera in *com-del-comando* un messaggio per le Clan Battle.', inline = False)
    embed.add_field(name = '`cb giorno orario1 orario2...`', value = 'Genera in *com-del-comando* un messaggio per le Clan Brawl.', inline = False)
    embed.add_field(name = '`edit channelID messageID "messaggio"`', value = 'modifica un messaggio con *messaggio*.', inline = False)
    embed.add_field(name = '`vote`', value = 'Aggiunge delle reazioni all\'ultimo messaggio inviato dall\'autore.', inline = False)
    await ctx.send(embed = embed)

@bot.command()
async def CB(ctx, *args):
    channel = bot.get_channel(comandoID)
    day = args[0]
    i = 1
    message = '<@&680766615234543662> perfavore segnalateci la vostra disponibilità per le Clan Battle!'
    await channel.send(message)
    while i < len(args):
            hour = args[i]
            message = 'Presenze delle Clan Battle di ' + day + ', ore: ' + hour
            msg = await channel.send(message)
            await msg.add_reaction('\U00002705')
            await msg.add_reaction('\U0000274C')
            await msg.add_reaction('\U0000267B')
            i = i + 1

@bot.command()
async def cb(ctx, *args):
    channel = bot.get_channel(comandoID)
    day = args[0]
    i = 1
    message = '<@&680766615234543662> perfavore segnalateci la vostra disponibilità per le Clan Brawl!'
    await channel.send(message)
    while i < len(args):
            hour = args[i]
            message = 'Presenze delle Clan Brawl di ' + day + ', ore: ' + hour
            msg = await channel.send(message)
            await msg.add_reaction('\U00002705')
            await msg.add_reaction('\U0000274C')
            await msg.add_reaction('\U0000267B')
            i = i + 1

@bot.command()
async def edit(ctx, channel_id, message_id, new_message):
    guild = ctx.guild
    channel = guild.get_channel(int(channel_id))
    message = await channel.fetch_message(int(message_id))
    await message.edit(content = new_message)

@bot.command()
async def vote(ctx):
    author = ctx.message.author
    channel = ctx.message.channel
    await ctx.message.delete()
    msg = await channel.history().get(author = author)
    await msg.add_reaction('\U00002705')
    await msg.add_reaction('\U0000274C')

@bot.command()
async def randomize(ctx, message_id):
    guild = ctx.guild
    channel = guild.get_channel(int(comandoID))
    message = await channel.fetch_message(int(message_id))
    emoji = discord.utils.get(ctx.guild.emojis, name = 'rapax')
    reaction = discord.utils.get(message.reactions, emoji = emoji)
    users = await reaction.users().flatten()
    partecipanti = len(users)
    squadre = int(partecipanti / 3)
    esclusi = partecipanti % 3
    message = 'Ci sono {} partecipanti. Le squadre sono composte da 3 giocatori, quindi ci saranno: \n - {} squadre; \n - {} partecipanti verranno esclusi.'.format(partecipanti, squadre, esclusi)
    await ctx.send(message)
    while len(users) >= 3:
        user1 = random.choice(users)
        users.remove(user1)
        user2 = random.choice(users)
        users.remove(user2)
        user3 = random.choice(users)
        users.remove(user3)
        await ctx.send('Team: ' + user1.name + ', ' + user2.name + ', ' + user3.name + '.')

    message = 'Gli esclusi sono: '
    while users:
        user = random.choice(users)
        users.remove(user)
        message = message + '\n - ' + user.name

    message = message + '.'
    if esclusi > 0:
        await ctx.send(message)

@bot.command()
async def dice(ctx):
    dado = [1, 2, 3, 4, 5, 6]
    await ctx.send(random.choice(dado))

@bot.command()
async def coin(ctx):
    moneta = ['Testa', 'Croce']
    await ctx.send(random.choice(moneta))

bot.run(TOKEN)
