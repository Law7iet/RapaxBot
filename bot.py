import discord
from discord.ext import commands
import config
from utils import *

if __name__ == "__main__":

    # Bot's setup
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix = config.data["PREFIX"], intents = intents)
    bot.remove_command("help")

    extensions = ["mod", "entmt"]
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))

    # Run bot
    bot.run(config.data["TOKEN"])
