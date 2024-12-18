from os import system
from disnake import Intents, HTTPException, ApplicationCommandInteraction
from disnake.ext import commands

from settings import config
from utils.constants import IMPERIUM_GUILD

if __name__ == "__main__":

    # Bots setup
    intents = Intents.default()
    intents.members = True
    bot = commands.InteractionBot(intents=intents,
                                  test_guilds=[IMPERIUM_GUILD])
    extensions = ["moderation", "nickname", "event"]
    for extension in extensions:
        try:
            bot.load_extension("extensions." + extension)
        except Exception as error:
            print(f"{extension} cannot be loaded. [{error}]")

    # Bot test slash command
    @bot.slash_command(description="Pong!")
    async def ping(inter: ApplicationCommandInteraction):
        await inter.response.send_message("Pong! `" + str(round(bot.latency * 1000)) + "ms`")


    # Run bot
    try:
        bot.run(config.data["DISCORD_TOKEN"])
    except HTTPException as e:
        if e.status == 429:
            print("Discord servers denied the connection: too many requests")
            print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
            system("python ./settings/restarter.py")
            system('kill 1')
        else:
            raise e
