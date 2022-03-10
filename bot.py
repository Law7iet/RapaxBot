import config
from discord import Intents, Embed, Activity, ActivityType
from discord.ext import commands

if __name__ == "__main__":

    # Bot's setup
    intents = Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix = config.data["PREFIX"], intents = intents, activity = Activity(type = ActivityType.watching, name = "la tua webcam."))
    bot.remove_command("help")

    @bot.command()
    async def help(ctx):
        embed = Embed(color=0xffd519)
        embed.description = "Il prefisso da usare è: `>`."
        embed.set_author(name = "RapaxBot", icon_url = "https://cdn.discordapp.com/attachments/675275973918195712/924566156407341076/Logo_RAPAX_Cerchio.png")
        embed.add_field(name = "`CB giorno`", value = "Genera in *com-del-comando* un messaggio per le presenze delle Clan Battle per il giorno *giorno*.", inline = False)
        embed.add_field(name = "`cb giorno`", value = "Genera in *com-del-comando* un messaggio per le presenze delle Clan Brawl per il giorno *giorno*.", inline = False)
        embed.add_field(name = "`write channel_id message`", value = "Scrive il *message* nel canale con ID *channel_id*", inline = False)
        embed.add_field(name = "`edit channel_id message_id messagge`", value = "Sostituisce il messaggio del bot scritto nel canale con ID *channel_id* con ID *message_id* col testo *messagge*.", inline = False)
        embed.add_field(name = "`add_emoji message_ID emoji`", value = "Aggiunge la reazione *emoji* al messaggio con ID *message_ID*.", inline = False)
        embed.add_field(name = "`vote message_id`", value = "Aggiunge le reazioni per votare al messaggio con ID *message_id*.", inline = False)
        embed.add_field(name = "`prison @member timer reason`", value = "Aggiunge il ruolo `Prigioniero` a ``@member` per `timer` secondi.", inline = False)
        embed.add_field(name = "`torp @member`", value = "Aggiunge il ruolo `Torpamici` a `@member` per un\"ora.", inline = False)
        embed.add_field(name = "`nickname`", value = "Cambia il nickname dei membri che hanno il tag *ospiti* col loro nickname di gioco.", inline = False)
        embed.add_field(name = "`ping`", value = "Pong!", inline = False)
        embed.add_field(name = "`dice number`", value = "Lancia un dado a `number` facce.", inline = False)
        embed.add_field(name = "`coin`", value = "Lancia una moneta.", inline = False)
        embed.set_footer(text = "WiP! Alcuni comandi potrebbero essere differenti. Per avere l\"ID di un messaggio o canale, bisogna attivare la modalità sviluppatore su Discord." )
        await ctx.send(embed = embed)

    extensions = ["moderator", "entertainment", "event"]
    for extension in extensions:
        try:
            bot.load_extension("extensions." + extension)
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))

    # Run bot
    bot.run(config.data["TOKEN"])
