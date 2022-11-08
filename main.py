from settings import config
from settings.keep_alive import keep_alive
from disnake import Intents, HTTPException, ApplicationCommandInteraction
from disnake.ext import commands
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

    @bot.slash_command(description="Pong!")
    async def ping(inter: ApplicationCommandInteraction):
        await inter.response.send_message("Pong! `" +
                                          str(round(bot.latency * 1000)) +
                                          "ms`")

    # Run bot
    try:
        keep_alive()
        bot.run(config.data["DISCORD_TOKEN"])
    except HTTPException as e:
        if e.status == 429:
            print("Discord servers denied the connection: too many requests")
            print("Stop the process with \"kill 1\"")
        else:
            raise e
