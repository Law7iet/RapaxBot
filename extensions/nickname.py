from disnake.ext import commands, tasks
from disnake import ApplicationCommandInteraction
from utils.functions import send_response_and_clear, check_role
from utils.constants import AuthorizationLevelEnum, CH_TXT_TESTING, IMPERIUM, IMPERIUM_GUILD
from utils.apiWargaming import ApiWargaming
import re
from datetime import time


class Nickname(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.apiWargaming = ApiWargaming()
        # Avvia la task automatica
        self.daily_nickname_task.start()

    @tasks.loop(time=time(3, 0))  # Esegui ogni giorno alle 3:00
    async def daily_nickname_task(self):
        """Task automatica per aggiornare i nickname."""
        guild = self.bot.get_guild(IMPERIUM_GUILD)
        if guild:
            testing_channel = guild.get_channel(CH_TXT_TESTING)
            if testing_channel:
                await testing_channel.send(":hourglass: Inizio aggiornamento automatico dei nickname...")
                await self._update_nicknames(guild, testing_channel)
                await testing_channel.send(":white_check_mark: Aggiornamento completato!")

    @daily_nickname_task.before_loop
    async def before_daily_nickname_task(self):
        """Assicura che la task inizi solo dopo che il bot è pronto."""
        await self.bot.wait_until_ready()
        print("Task giornaliera per aggiornare i nickname pronta.")

    async def _update_nicknames(self, guild, testing_channel):
        """Logica principale condivisa per aggiornare i nickname."""
        members = guild.members
        for member in members:
            # Solo se il membro ha il ruolo OSPITI
            if guild.get_role(IMPERIUM) in member.roles:
                tmp = re.sub(r"\[.+\]", "", member.display_name)
                tmp = re.sub(r"\(.+\)", "", tmp)
                user_current_nickname = tmp.lstrip().rstrip()
                try:
                    user_current_tag = re.search(r"\[.+\]", member.display_name).group(0)[1:-1]
                except:
                    user_current_tag = ''
                try:
                    user_current_name = re.search(r"\(.+\)", member.display_name).group(0)
                except:
                    user_current_name = ''
                try:
                    # Cerca il nickname e il clan tramite l'API WoWs
                    player_info = self.apiWargaming.get_player_by_nick(user_current_nickname)
                    if player_info is None:
                        await testing_channel.send(f":exclamation: <@{member.id}> non trovato.")
                        continue
                    clan_id = self.apiWargaming.get_clan_by_player_id(player_info[0])
                    if clan_id == -1:
                        await testing_channel.send(f"Errore API WG: `get_clan_by_player_id({player_info[0]})`")
                        continue
                    if clan_id is None:
                        await testing_channel.send(f":warning: <@{member.id}> non fa parte di nessun clan.")
                    else:
                        clan_info = self.apiWargaming.get_clan_name_by_id(clan_id)
                        if clan_info is None:
                            await testing_channel.send(f":grey_question: <@{member.id}> ha il tag `@Imperium` ma non ha un clan.")
                        elif clan_info[1] != user_current_tag:
                            user_current_tag = clan_info[1]
                            await testing_channel.send(f":white_check_mark: <@{member.id}> cambiato tag `{clan_info[1]}`")
                    if user_current_nickname != player_info[1]:
                        user_current_nickname = player_info[1]
                    if user_current_tag != '':
                        user_current_tag = f"[{user_current_tag}] "
                    new_nickname = user_current_tag + user_current_nickname + " " + user_current_name
                    if len(new_nickname) > 32:
                        new_nickname = user_current_tag + " " + user_current_nickname
                    await member.edit(nick=new_nickname)
                except:
                    await testing_channel.send(f":bangbang: <@{member.id}> errore.")

    @commands.slash_command(description="Cambia il nickname degli utenti del server con quello di WoWs.")
    async def nickname(self, inter: ApplicationCommandInteraction) -> None:
        """Comando manuale per aggiornare i nickname."""
        await inter.response.defer()
        if not (await check_role(inter, AuthorizationLevelEnum.CONSOLE)):
            await send_response_and_clear(inter, False, "Non hai i permessi.")
            return
        guild = inter.guild
        testing_channel = guild.get_channel(CH_TXT_TESTING)
        await self._update_nicknames(guild, testing_channel)
        await send_response_and_clear(inter, True, "Fatto!")


def setup(bot: commands.Bot):
    bot.add_cog(Nickname(bot))
