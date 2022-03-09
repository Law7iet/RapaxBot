import re
from apiWarGaming import ApiWarGaming
from discord import Embed, Emoji
from discord.ext import commands
from discord.utils import get
from utils import *

class Moderator(commands.Cog):

    def __init__(self, bot: commands.Cog):
        self.bot = bot
        self.apiWargaming = ApiWarGaming()
    
    async def presenze(self, ctx: commands.context.Context, type: WowsEventEnum, message: str) -> None:
        """
        Generate the partecipation message for Clan Battles, Clan Brawl, Training or other events.
        Each event is associated with the `WowsEventEnum` enum and each event has a own reaction.
        The keys are separed from the message by 3 new lines; using 3 new lines in a row you wont be able to edit the description.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `type` (WowsEventEnum): type of the event.
            `message` (str): the message which will be displayed in the embed as description.

        Returns:
            `None`
        """
        if not(await checkRole(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None

        channel = self.bot.get_channel(CH_TXT_COM_DEL_COMANDO)
        ping = "<@&" + str(MEMBRO_DEL_CLAN) + ">"
        # TEST MODE
        # channel = self.bot.get_channel(CH_TXT_TESTING)
        # ping = "<@&" + str(OSPITI) + ">"

        title = "Presenze " + wowsEvent[int(type)]
        if type == WowsEventEnum.CLAN_BATTLE:
            keys = CBKeys
            reactions = CBEmoji
            icon = "https://cdn.discordapp.com/attachments/675275973918195712/951066454596419604/clanBattle.png"
        elif type == WowsEventEnum.CLAN_BRAWL:
            keys = CBKeys
            reactions = CBEmoji
            icon = "https://cdn.discordapp.com/attachments/675275973918195712/951066455032598578/clanBrawl.png"
        elif type == WowsEventEnum.TRAINING:
            keys = eventKeys
            reactions = eventEmoji
            icon = "https://cdn.discordapp.com/attachments/675275973918195712/944964438652506192/training.png"
        elif type == WowsEventEnum.OTHER:
            keys = voteKeys
            reactions = voteEmoji
            icon = 'https://cdn.discordapp.com/attachments/675275973918195712/944988546811461653/rapax.png'
        else:
            return None
        embed = Embed(title = title, description = message + "\n\n\n" + "\n".join(keys), color = 0xffd519)
        embed.set_author(name = "RapaxBot")
        embed.set_thumbnail(url = icon)

        await channel.send(ping)
        msg = await channel.send(embed = embed)
        for element in reactions:
            await msg.add_reaction(element)
    
    @commands.command()
    async def edit_embed(self, ctx: commands.context.Context, channelId: int, messageId: int, *, newDescription: str) -> None:
        """
        Edit the description of a embed message.
        The old description has one '3 new lines' to separe the own message and the keys. 

        Args:
            `ctx` (commands.context.Context): it's the context.
            `channelId` (int): the channel's ID where the message was sent.
            `messageId` (int): the message ID.
            `newDescription` (str): the new description of the embed.

        Returns:
            `None`
        """        
        if not(await checkRole(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None
        guild = ctx.guild
        channel = guild.get_channel(channelId)
        message = await channel.fetch_message(messageId)
        try:
            embed = message.embeds[0]
            oldDescription = embed.description.split('\n\n\n')
            oldDescription[0] = newDescription
            description = oldDescription[0] + '\n\n\n' + oldDescription[1]
            embed.description = description
            await message.edit(embed = embed)
        except:
            return None

    @commands.command()
    async def write(self, ctx: commands.context.Context, channelId: int, *, message: str) -> None:
        """
        Write a message using the bot profile.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `channelId` (int): the channel's ID where you want to write.
            `message` (str): the message you want to write.

        Returns:
            `None`
        """        
        if not(await checkRole(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None
        guild = ctx.guild
        channel = guild.get_channel(channelId)
        await channel.send(message)

    @commands.command()
    async def edit(self, ctx: commands.context.Context, channelId: int, messageId: int, *, newMessage: str) -> None:
        """
        Edit a message sent by the bot.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `channelId` (int): the channel's ID where the message was sent.
            `messageId` (int): the message ID.
            `newMessage` (str): the new message.

        Returns:
            `None`
        """        
        if not(await checkRole(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None
        guild = ctx.guild
        channel = guild.get_channel(channelId)
        message = await channel.fetch_message(messageId)
        await message.edit(content = newMessage)

    @commands.command()
    async def add_emoji(self, ctx: commands.context.Context, channelId: int, messageId: int, emoji: Emoji) -> None:
        """
        Add a reaction to a message. It works only for default's emoji and server's emoji.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `channelId` (int): the channel's ID where the message was sent.
            `messageId` (int): the message ID which you want to add a reaction.
            emoji (Emoji): the emoji you want to use as reaction.

        Returns:
            `None`
        """        
        if not(await checkRole(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None
        channel = ctx.message.channel
        await ctx.message.delete()
        message = await channel.fetch_message(messageId)
        await message.add_reaction(emoji)
    
    @commands.command()
    async def CB(self, ctx: commands.context.Context, *, message: str) -> None:
        """
        Sent an embed that requests the partecipation of the Clan Battle.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `message` (str): it's the message that compares in the embed as description.

        Returns:
            `None`
        """        
        await self.presenze(ctx, WowsEventEnum.CLAN_BATTLE, message)
    
    @commands.command()
    async def cb(self, ctx: commands.context.Context, *, message: str) -> None:
        """
        Sent an embed that requests the partecipation of the Clan Brawl.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `message` (str): it's the message that compares in the embed as description.
        
        Returns:
            `None`
        """  
        await self.presenze(ctx, WowsEventEnum.CLAN_BRAWL, message)

    @commands.command()
    async def training(self, ctx: commands.context.Context, *, message: str) -> None:
        """
        Sent an embed that requests the partecipation of the training.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `message` (str): it's the message that compares in the embed as description.
        
        Returns:
            `None`
        """
        await self.presenze(ctx, WowsEventEnum.TRAINING, message)

    @commands.command()
    async def event(self, ctx: commands.context.Context, *, message: str) -> None:
        """
        Sent an embed that requests the partecipation of a event.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `message` (str): it's the message that compares in the embed as description.

        Returns:
            `None`
        """  
        await self.presenze(ctx, WowsEventEnum.OTHER, message)

    @commands.command()
    async def nickname(self, ctx: commands.context.Context) -> None:
        """
        Check the server's guests' nickname and role.
        The bot change their nickname with their game nickname, using their current nickname.
        It adds the clans tag at the beginning.
        Each clan has a role, if not, it creates it and add it to the member.

        Args:
            ctx (commands.context.Context): it's the context.
        
        Returns:
            `None`
        """  
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
