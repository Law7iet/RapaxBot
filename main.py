from os import system
from settings import config
from settings.keep_alive import keep_alive
from disnake import Intents, HTTPException, ApplicationCommandInteraction
from disnake.ext import commands, tasks
from utils.constants import RAPAX_GUILD

if __name__ == "__main__":

    # Bots setup
    intents = Intents.default()
    intents.members = True
    bot = commands.InteractionBot(intents=intents,
                                  test_guilds=[RAPAX_GUILD])
    extensions = ["moderation", "entertainment", "event", "nickname"]
    for extension in extensions:
        try:
            bot.load_extension("extensions." + extension)
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))

    # Bot test slash command
    @bot.slash_command(description="Pong!")
    async def ping(inter: ApplicationCommandInteraction):
        await inter.response.send_message("Pong! `" + str(round(bot.latency * 1000)) + "ms`")

    # Bot loop
    @tasks.loop(seconds=10.0)
    async def foo():
        return

    # Run bot
    try:
        keep_alive()
        bot.run(config.data["DISCORD_TOKEN"])
    except HTTPException as e:
        if e.status == 429:
            print("Discord servers denied the connection: too many requests")
            print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
            system("python restarter.py")
            system('kill 1')
        else:
            raise e
