from utils import *
import moderator as mod
import random
import discord
import asyncio

#@bot.event
#async def on_ready():
#    channel = bot.get_channel(testing_ID)
#    message = 'RapaxBot è pronto a salpare!'
#    await channel.send(message)

@bot.command()
async def help(ctx):
    embed = discord.Embed()
    embed.colour = discord.Colour.from_rgb(152, 4, 11)
    embed.description = 'Il prefisso da usare è: `>`\n `[]` indica un parametro opzionale. \n `{}` indica un parametro ripetibile.'
    embed.set_author(name = 'RapaxBot', icon_url = 'https://cdn.discordapp.com/attachments/711212263062765608/781507702853074964/Rapax_circle.png')
    embed.add_field(name = '`CB day time {time}`', value = 'Genera in *com-del-comando* un messaggio per le Clan Battle.', inline = False)
    embed.add_field(name = '`cb day time {time}`', value = 'Genera in *com-del-comando* un messaggio per le Clan Brawl.', inline = False)
    embed.add_field(name = '`write channel_ID "message"`', value = 'Scrive il *message* nel canale con ID *channel_ID*', inline = False)
    embed.add_field(name = '`edit channel_ID message_ID "messagge"`', value = 'Sostituisce il messaggio con ID *message_ID* col testo *messagge*.', inline = False)
    embed.add_field(name = '`add_emoji message_ID [emoji]`', value = 'Aggiunge la reazione *emoji* al messaggio con ID *message_ID*.', inline = False)
    embed.add_field(name = '`vote [message_ID]`', value = 'Aggiunge le reazioni per votare all\'ultimo messaggio inviato dall\'autore, o al messaggio con ID *message_ID*.', inline = False)
    embed.add_field(name = '`ban @member timer "reason"`', value = 'Aggiunge il ruolo `Prigioniero` a ``@member` per `timer` secondi', inline = False)
    embed.add_field(name = '`dice`', value = 'Lancia un dado a 6 facce.', inline = False)
    embed.add_field(name = '`d20`', value = 'Lancia un dado a 20 facce.', inline = False)
    embed.add_field(name = '`coin`', value = 'Lancia una moneta.', inline = False)
    embed.set_footer(text = 'Per avere l\'ID di un messaggio o canale, bisogna attivare la modalità sviluppatore su Discord.' )
    await ctx.send(embed = embed)

@bot.command()
async def CB(ctx, *args):
    flag = mod.check_role(ctx)
    if flag == True:
        channel = bot.get_channel(testing_ID)
        i = 1
        message = mod.clan_message(1)
        await channel.send(message)
        while i < len(args):
                message = mod.clan_participation(1, args[0], args[i])
                msg = await channel.send(message)
                for element in votazioni_cb:
                    await msg.add_reaction(element)
                i = i + 1
    else:
        await ctx.message.delete()
        await ctx.send('Non hai i permessi')

@bot.command()
async def cb(ctx, *args):
    flag = mod.check_role(ctx)
    if flag == True:
        channel = bot.get_channel(testing_ID)
        i = 1
        message = mod.clan_message(0)
        await channel.send(message)
        while i < len(args):
                message = mod.clan_participation(0, args[0], args[i])
                msg = await channel.send(message)
                for element in votazioni_cb:
                    await msg.add_reaction(element)
                i = i + 1
    else:
        await ctx.message.delete()
        await ctx.send('Non hai i permessi')

@bot.command()
async def write(ctx, channel_id, message):
    flag = mod.check_role(ctx)
    if flag == True:
        guild = ctx.guild
        channel = guild.get_channel(int(channel_id))
        await channel.send(message)
    else:
        await ctx.message.delete()
        await ctx.send('Non hai i permessi')

@bot.command()
async def edit(ctx, channel_id, message_id, new_message):
    flag = mod.check_role(ctx)
    if flag == True:
        guild = ctx.guild
        channel = guild.get_channel(int(channel_id))
        message = await channel.fetch_message(int(message_id))
        await message.edit(content = new_message)
    else:
        await ctx.message.delete()
        await ctx.send('Non hai i permessi')

@bot.command()
async def add_emoji(ctx, message_id, emoji):
    flag = mod.check_role(ctx)
    if flag == True:
        guild = ctx.guild
        channel = ctx.message.channel
        await ctx.message.delete()
        message = await channel.fetch_message(int(message_id))
        await message.add_reaction(emoji)
    else:
        await ctx.message.delete()
        await ctx.send('Non hai i permessi')

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
        flag = mod.check_role(ctx)
        if flag == True:
            message_id = args[0]
            channel = ctx.message.channel
            msg = await channel.fetch_message(int(message_id))
            for element in votazioni:
                await msg.add_reaction(element)
        else:
            await ctx.message.delete()
            await ctx.send('Non hai i permessi')

@bot.command()
async def dice(ctx):
    dado = [1, 2, 3, 4, 5, 6]
    await ctx.send(random.choice(dado))

@bot.command()
async def d20(ctx):
    dado = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    await ctx.send(random.choice(dado))

@bot.command()
async def coin(ctx):
    moneta = ['Testa', 'Croce']
    await ctx.send(random.choice(moneta))

@bot.command()
async def ban(ctx, member: discord.Member, time, message):
    flag = mod.check_role(ctx)
    if flag == True:
        guild = ctx.guild
        channel = guild.get_channel(int(783375373285982208))
        role = guild.get_role(783375143593836595)
        list_roles = member.roles
        for i in range(1, len(list_roles)):
            await member.remove_roles(list_roles[i])
        await member.add_roles(role)
        message = member.name + ' è stato messo in prigione per ' + time + ' secondi.\nMovitazione: ' + message
        await channel.send(message)
        timer = int(time)
        while True:
            timer -= 1
            if timer == 0:
                await channel.send('Fine quarantena.')
                break
            await asyncio.sleep(1)
        for i in range(1, len(list_roles)):
            await member.add_roles(list_roles[i])
        await member.remove_roles(role)
    else:
        await ctx.message.delete()
        await ctx.send('Non hai i permessi')

@bot.command()
async def randomize(ctx, message_id):
    guild = ctx.guild
    channel = guild.get_channel(int(comando_ID))
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

@bot.command()
async def ciao(ctx, member: discord.Member):
    lista = member.roles
    print(lista[0])
    print(type(lista[0]))

bot.run(TOKEN)
