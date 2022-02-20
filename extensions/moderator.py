import re
from apiWarGaming import ApiWarGaming
from discord import Embed, Emoji
from discord.ext import commands
from discord.utils import get
from utils import *

class Moderator(commands.Cog):
    
    reclutatori = [
        396025435625881613,
        354711274849959937,
        256858029390168064,
        284818538475159562
    ]

    CBEmoji = (
        "\U00000031\U000020E3",
        "\U00000032\U000020E3",
        "\U0001F557", 
        "\U0000274C",
        "\U00002753"
    )

    CBKeys = (
        "- \U00000031\U000020E3 19:00-21:00", 
        "- \U00000032\U000020E3 21:00-23:00", 
        "- \U0001F557 Arrivo tardi", 
        "- \U0000274C Non disponibile", 
        "- \U00002753 Forse"
    )

    def __init__(self, bot: commands.Cog):
        self.bot = bot
        self.apiWargaming = ApiWarGaming()
    
    # Generate the partecipation message for Clan Battles or Clan Brawl
    async def presenze(self, ctx: commands.context.Context, type: WoWsEventEnum, *, day: str):
        if not(await checkRole(ctx)):
            return None

        channel = self.bot.get_channel(CH_TXT_COM_DEL_COMANDO)
        message = "<@&" + str(MEMBRO_DEL_CLAN) + ">"
        # TEST MODE
        channel = self.bot.get_channel(CH_TXT_TESTING)
        message = "<@&" + str(OSPITI) + ">"

        embed=Embed(title = "Presenze " + type, description = day + "\n\n" + "\n".join(self.CBKeys), color = 0xffd519)
        embed.set_author(name="RapaxBot")
        if type == WoWsEventEnum.CLAN_BATTLE:
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/675275973918195712/944874666164637736/clanBattle.png")
        elif type == WoWsEventEnum.CLAN_BRAWL:
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/675275973918195712/944874666391142500/clanBrawl.png")
        else:
            return None

        await channel.send(message)
        msg = await channel.send(embed = embed)
        for element in self.CBEmoji:
            await msg.add_reaction(element)

    @commands.command()
    async def write(self, ctx: commands.context.Context, channelId: int, *, message: str):
        if not(await checkRole(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None
        guild = ctx.guild
        channel = guild.get_channel(channelId)
        await channel.send(message)

    @commands.command()
    async def edit(self, ctx: commands.context.Context, channelId: int, messageId: int, *, newMessage: str):
        if not(await checkRole(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None
        guild = ctx.guild
        channel = guild.get_channel(channelId)
        message = await channel.fetch_message(messageId)
        await message.edit(content = newMessage)

    # It works only for deafult's emoji and server's emoji
    @commands.command()
    async def add_emoji(self, ctx: commands.context.Context, messageId: int, emoji: Emoji):
        if not(await checkRole(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None
        channel = ctx.message.channel
        await ctx.message.delete()
        message = await channel.fetch_message(messageId)
        await message.add_reaction(emoji)
    
    @commands.command()
    async def CB(self, ctx, *day):
        await self.presenze(ctx, WoWsEventEnum.CLAN_BATTLE, day)
    
    @commands.command()
    async def cb(self, ctx, *day):
        await self.presenze(ctx, WoWsEventEnum.CLAN_BRAWL, day)

    @commands.command()
    async def nickname(self, ctx: commands.context.Context):
        if not(await checkRole(ctx, AuthorizationLevelEnum.AMMINISTRATORE)):
            return None
        guild = ctx.guild
        members = guild.members
        # For each member of the server
        for member in members:
            # Only if the member has OSPITI role
            if guild.get_role(OSPITI) in member.roles:
                # Get Discord's member nick
                # Split tag, nick and name
                tmp = re.sub(r"\[.+\]", "", member.display_name)
                tmp = re.sub(r"\(.+\)", "", tmp)
                userCurrentNickname = tmp.lstrip().rstrip()
                try:
                    user_current_tag = re.search("\[.+\]", member.display_name).group(0)[1:-1]
                except:
                    user_current_tag = ''                
                try:
                    user_current_name = re.search("\(.+\)", member.display_name).group(0)
                except:
                    user_current_name = ''

                try:
                    # search nick with WoWs API
                    player_info = self.apiWargaming.getPlayerByNick(userCurrentNickname)
                    if player_info == None:
                        await ctx.send("\U000026A0 Il membro `" + member.display_name + "` non è stato trovato.")
                        continue
                    # search tag with WoWs API
                    clan_id = self.apiWargaming.getClanByPlayerId(player_info[0])
                    
                    # DEBUG
                    # print(user_current_nickname + ": " + str(clan_id))
                    
                    if clan_id == None:
                        # The player has not a clan
                        pass
                    else:
                        # The player has a clan
                        # Check if the role exists, else create it
                        clan_info = self.apiWargaming.getClanNameById(clan_id)
                        if(get(guild.roles, name=clan_info[0]) == None):
                            await guild.create_role(name = clan_info[0], hoist = True, reason = 'Tag del Clan')
                            await ctx.send("\U0001F464 nuovo tag: `" + clan_info[0] + "`")
                        # Change user tag
                        if clan_info[1] != user_current_tag:
                            user_current_tag = clan_info[1]
                            await ctx.send("\U00002705 `" + member.display_name + "` cambiato tag `" + clan_role.name + "`")
                        # Change user role
                        # TO-DO: Compute and remove the old role
                        # Add the role
                        clan_role = get(guild.roles, name=clan_info[0])
                        if not(clan_role in member.roles):                            
                            await member.add_roles(clan_role, reason="Clan Tag")
                            await ctx.send("\U00002705 `" + member.display_name + "` aggiunto il ruolo `" + clan_role.name + "`")

                    # Change user nickname
                    if userCurrentNickname != player_info[1]:
                        userCurrentNickname = player_info[1]
                    # set ready the new full nickname
                    if user_current_tag != '':
                        user_current_tag = "[" + user_current_tag + "] "
                    new_nickname = user_current_tag + userCurrentNickname + " " + user_current_name
                    if len(new_nickname) > 32:
                        new_nickname = user_current_tag + " " + userCurrentNickname
                    # Edit member
                    await member.edit(nick=new_nickname)
                
                except:
                    await ctx.send("\U0000203C `" + member.display_name + "` non è stato trovato.")

        await ctx.send("\U0001F60A Fine!")

def setup(bot: commands.Cog):
    bot.add_cog(Moderator(bot))
