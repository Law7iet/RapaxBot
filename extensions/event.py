from discord import Member
from discord.ext import commands
from utils.constants import *


class Event(commands.Cog):
    def __init__(self, bot: commands.Cog):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, user: Member):
        guild = self.bot.get_guild(RAPAX_GUILD)
        members = guild.members
        for member in members:
            recruiter_role = guild.get_role(RECLUTATORE)
            if recruiter_role in member.roles:
                await member.send(user.name + " è entrato nel server " + guild.name + ".")

        message = "Ciao " + user.name + ", benvenuto nel clan " + guild.name + ".\n" + '''
Gli ufficiali del clan saranno onorati di intrattenerti ed illustrarti perché questo clan è uno dei migliori clan italiani per l'insieme delle caratteristiche che noi riteniamo vincenti: simpatia, piacere del gioco, correttezza, condivisione, spirito competitivo, assenza di preconcetti e disponibilità verso tutti i giocatori di qualunque livello, capacità ed esperienza.
Nel rispetto di tutti i membri del server, leggi attentamente il *regolamento* del server.
Per una migliore comunicazione nel server, ti inviamo a modificare il proprio nickname col tag del proprio clan (racchiuso fra le parentesi quadre) seguito da uno spazio e il nickname di battaglia.
Ci auguriamo che questa occasione ti porti a rimanere in questo clan per molto, molto tempo. Buon divertimento!
'''
        await user.send(message)

    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member, before, after):
    #     channel = before.channel or after.channel

    #     if channel.id == CH_VCL_PLANCIA_PUBBLICA:
    #         if before.channel is None and after.channel is not None:
    #             if member.id == 256858029390168064:
    #                 await self.bot.get_channel(CH_TXT_COM_TRA_MEMBRI).send("Bonotz85 è entrato nel canale vocale *plancia pubblica*")


def setup(bot: commands.Cog):
    bot.add_cog(Event(bot))
