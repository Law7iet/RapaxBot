from disnake import Member
from disnake.ext import commands, tasks

from utils.constants import IMPERIUM_GUILD


class Event(commands.Cog):
    def __init__(self, bot: commands.Cog):
        self.bot = bot
        self.current_count = 0  # Conteggio corrente
        self.voice_channel_id = 1314498879957499954  # Sostituisci con l'ID del canale vocale "PIPPO"
        self.afk_channel_id = 680765700159045730  # Sostituisci con l'ID del canale AFK
        self.guild_id = IMPERIUM_GUILD  # Sostituisci con l'ID della tua guild
        self.update_task.start()  # Avvia la task ricorrente

    # @commands.Cog.listener()
    # async def on_member_join(self, user: Member):
    #     guild = self.bot.get_guild(IMPERIUM_GUILD)
    #     members = guild.members
    #     for member in members:
    #         recruiter_role = guild.get_role(RECLUTATORE)
    #         if recruiter_role in member.roles:
    #             await member.send(user.name + " è entrato nel server " +
    #                               guild.name + ".")

    #     message = "Ciao " + user.name + ", benvenuta/o in Imperium. \n" +\
    #     '''I consoli e i senatori saranno onorati di intrattenerti ed
    #     illustrarti perché questo server è uno dei migliori in Italia per 
    #     l'insieme delle caratteristiche che noi riteniamo vincenti: simpatia,
    #     piacere del gioco, correttezza, condivisione, spirito competitivo, 
    #     assenza di preconcetti e disponibilità verso tutti i giocatori di 
    #     qualunque livello, capacità ed esperienza. Nel rispetto di tutti i 
    #     membri del server, leggi attentamente il *regolamento* del server. Per 
    #     una migliore comunicazione nel server, ti inviamo a modificare il 
    #     proprio nickname col tag del proprio clan (racchiuso fra le parentesi 
    #     quadre) seguito da uno spazio e il nickname di battaglia.\n Ci 
    #     auguriamo che questa occasione ti porti a rimanere in questo server per 
    #     molto, molto tempo. Buon divertimento!'''
    #     await user.send(message)

    @tasks.loop(minutes=10)  # Intervallo di aggiornamento (10 secondi)
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
