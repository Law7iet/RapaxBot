from disnake.ext import commands
from disnake import ApplicationCommandInteraction
from utils.functions import send_response_and_clear, check_role
from utils.constants import AuthorizationLevelEnum, CH_TXT_TESTING, OSPITI, DEBUG
from utils.apiWargaming import ApiWargaming
import re


class Nickname(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.apiWargaming = ApiWargaming()

    @commands.slash_command(
        description=
        "Cambia il nickname degli utenti del server con quello di WoWs.")
    async def nickname(self, inter: ApplicationCommandInteraction) -> None:
        """
        Check the server's guests' nickname. The bot change their nickname with
        their game nickname, using their current nickname. It adds the clans
        tag at the beginning.

        Args:
            inter: the application command interation (context).

        Returns:
            None
        """
        await inter.response.defer()
        if not (await check_role(inter,
                                 AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            await send_response_and_clear(inter, False, "Non hai i permessi.")
            return
        guild = inter.guild
        testing_channel = guild.get_channel(CH_TXT_TESTING)
        members = guild.members
        for member in members:
            # Only if the member has OSPITI role
            if guild.get_role(OSPITI) in member.roles:
                # Get Discord's member nick
                # Split tag, nick and name
                tmp = re.sub(r"\[.+\]", "", member.display_name)
                tmp = re.sub(r"\(.+\)", "", tmp)
                user_current_nickname = tmp.lstrip().rstrip()
                try:
                    user_current_tag = re.search(
                        "\[.+\]", member.display_name).group(0)[1:-1]
                except:
                    user_current_tag = ''
                try:
                    user_current_name = re.search("\(.+\)",
                                                  member.display_name).group(0)
                except:
                    user_current_name = ''
                try:
                    # search nick with WoWs API
                    player_info = self.apiWargaming.get_player_by_nick(
                        user_current_nickname)
                    if player_info is None:
                        await testing_channel.send("\U000026A0 Il membro `" +
                                                   member.display_name +
                                                   "` non è stato trovato.")
                        continue
                    # search tag with WoWs API
                    clan_id = self.apiWargaming.get_clan_by_player_id(
                        player_info[0])

                    if DEBUG:
                        print(user_current_nickname + ": " + str(clan_id))

                    if clan_id is None:
                        # The player has not a clan
                        pass
                    else:
                        # The player has a clan
                        # Add the tag to the user
                        clan_info = self.apiWargaming.get_clan_name_by_id(
                            clan_id)
                        if clan_info[1] != user_current_tag:
                            user_current_tag = clan_info[1]
                            await testing_channel.send("\U00002705 `" +
                                                       member.display_name +
                                                       "` cambiato tag `" +
                                                       clan_info[1] + "`")
                    # Change user nickname
                    if user_current_nickname != player_info[1]:
                        user_current_nickname = player_info[1]
                    if user_current_tag != '':
                        user_current_tag = "[" + user_current_tag + "] "
                    new_nickname = user_current_tag + user_current_nickname + " " + user_current_name
                    if len(new_nickname) > 32:
                        new_nickname = user_current_tag + " " + user_current_nickname
                    await member.edit(nick=new_nickname)

                except:
                    await testing_channel.send("\U0000203C `" +
                                               member.display_name +
                                               "` errore.")

        await send_response_and_clear(inter, True, "Fatto!")


def setup(bot: commands.Bot):
    bot.add_cog(Nickname(bot))
