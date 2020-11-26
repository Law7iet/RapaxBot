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
    embed.colour = discord.Colour.from_rgb(152, 4, 11)
    embed.description = 'Il prefisso da usare è: `>`\n `[]` indica un parametro opzionale. \n `{}` indica un parametro ripetibile.'
    embed.set_author(name = 'RapaxBot', icon_url = 'https://cdn.discordapp.com/attachments/711212263062765608/781507702853074964/Rapax_circle.png')
    embed.add_field(name = '`write channel_ID "message"`', value = 'Scrive il *message* nel canale con ID *channel_ID*', inline = False)
    embed.add_field(name = '`edit channel_ID message_ID "messagge"`', value = 'Sostituisce il messaggio con ID *message_ID* col testo *messagge*.', inline = False)
    embed.add_field(name = '`add_emoji message_ID [emoji]`', value = 'Aggiunge la reazione *emoji* al messaggio con ID *message_ID*.', inline = False)
    embed.add_field(name = '`vote [message_ID]`', value = 'Aggiunge le reazioni per votare all\'ultimo messaggio inviato dall\'autore, o al messaggio con ID *message_ID*.', inline = False)
    embed.add_field(name = '`CB day time {time}`', value = 'Genera in *com-del-comando* un messaggio per le Clan Battle.', inline = False)
    embed.add_field(name = '`cb day time {time}`', value = 'Genera in *com-del-comando* un messaggio per le Clan Brawl.', inline = False)
    embed.add_field(name = '`dice`', value = 'Lancia un dado a 6 facce.', inline = False)
    embed.add_field(name = '`coin`', value = 'Lancia una moneta.', inline = False)
    embed.set_footer(text = 'Per avere l\'ID di un messaggio o canale, bisogna attivare la modalità sviluppatore su Discord.' )
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
async def write(ctx, channel_id, message):
    guild = ctx.guild
    channel = guild.get_channel(int(channel_id))
    await channel.send(message)

@bot.command()
async def edit(ctx, channel_id, message_id, new_message):
    guild = ctx.guild
    channel = guild.get_channel(int(channel_id))
    message = await channel.fetch_message(int(message_id))
    await message.edit(content = new_message)

@bot.command()
async def add_emoji(ctx, message_id, emoji):
    guild = ctx.guild
    channel = ctx.message.channel
    message = await channel.fetch_message(int(message_id))
    await ctx.message.delete()
    await message.add_reaction(emoji)

@bot.command()
async def vote(ctx, *args):
    await ctx.message.delete()
    if len(args) == 0:
        author = ctx.message.author
        channel = ctx.message.channel
        msg = await channel.history().get(author = author)
    else:
        message_id = args[0]
        channel = ctx.message.channel
        msg = await channel.fetch_message(int(message_id))
    await msg.add_reaction('\U00002705')
    await msg.add_reaction('\U0000274C')

@bot.command()
async def dice(ctx):
    dado = [1, 2, 3, 4, 5, 6]
    await ctx.send(random.choice(dado))

@bot.command()
async def coin(ctx):
    moneta = ['Testa', 'Croce']
    await ctx.send(random.choice(moneta))

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
        await ctx.send('Team: ' + user1.nick + ', ' + user2.nick + ', ' + user3.nick + '.')
    message = 'Gli esclusi sono: '
    while users:
        user = random.choice(users)
        users.remove(user)
        message = message + '\n - ' + user.nick
    message = message + '.'
    if esclusi > 0:
        await ctx.send(message)

bot.run(TOKEN)
