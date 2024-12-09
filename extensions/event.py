from disnake.ext import commands, tasks
from utils.constants import IMPERIUM_GUILD, CH_VCL_IN_CANALE, CH_VCL_AFK


class Event(commands.Cog):
    def __init__(self, bot: commands.Cog):
        self.bot = bot
        self.current_count = 0
        self.voice_channel_id = CH_VCL_IN_CANALE
        self.afk_channel_id = CH_VCL_AFK
        self.guild_id = IMPERIUM_GUILD
        self.update_task.start()

    @tasks.loop(minutes=5)  # Intervallo di aggiornamento (5 minuti)
    async def update_task(self):
        # Ottieni la guild e i canali
        guild = self.bot.get_guild(self.guild_id)
        if not guild:
            return

        afk_channel = guild.get_channel(self.afk_channel_id)
        voice_channel_to_update = guild.get_channel(self.voice_channel_id)

        # Conta gli utenti nei canali vocali, escludendo il canale AFK
        total_voice_users = sum(len(channel.members) for channel in guild.voice_channels if channel != afk_channel)
        print(f"In canale: {total_voice_users}")
        # Aggiorna il nome del canale vocale se il conteggio è cambiato
        if voice_channel_to_update and total_voice_users != self.current_count:
            self.current_count = total_voice_users
            new_name = f"In canale: {total_voice_users}"
            await voice_channel_to_update.edit(name=new_name)
            print(f"Canale aggiornato: {new_name}")

    def cog_unload(self):
        # Ferma la task se il Cog viene rimosso
        self.update_task.cancel()


def setup(bot: commands.Cog):
    bot.add_cog(Event(bot))
