from disnake import Intents, TextInputStyle
from disnake.ext import commands
import disnake

import config

if __name__ == "__main__":

    # Bots setup
    intents = Intents.default()
    intents.members = True
    bot = commands.Bot(
            command_prefix=commands.when_mentioned_or(config.data["PREFIX"]),
            intents=intents
    )
    extensions = ["moderation", "entertainment", "event"]
    for extension in extensions:
        try:
            bot.load_extension("extensions." + extension)
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))

    # Run bot
    bot.run(config.data["TOKEN"])
