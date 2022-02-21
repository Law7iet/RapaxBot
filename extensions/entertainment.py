import asyncio
from discord import Embed, Member
from discord.ext import commands
from random import choice
from random import randrange
from utils.constants import *
from utils.functions import *

class Entertainment(commands.Cog):
    def __init__(self, bot: commands.Cog):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.context.Context) -> None:
        """
        A simple command that respons with "Pong!".

        Args:
            `ctx` (commands.context.Context): it's the context.
        
        Returns:
            `None`
        """        
        await ctx.send('Pong!')

    @commands.command()
    async def vote(self, ctx: commands.context.Context, channelId: int, messageId: int) -> None:
        """
        Add 3 reactions to the a message; the reactions are "\U00002705, \U0000274C, and \U00002753.
        If the message's author is the person who called this command, it add the emojis if the caller is at least an executive officer.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `channelId` (int): the channel's ID where the message was sent.
            `messageId` (int): the message ID where you want to add the reactions.

        Returns:
            `None`
        """
        author = ctx.message.author
        guild = ctx.guild
        channel = guild.get_channel(channelId)
        msg = await channel.fetch_message(messageId)
        if msg.author != author:
            if not(await checkRole(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
                return None
        await ctx.message.delete()
        for element in voteEmoji:
            await msg.add_reaction(element)

    @commands.command()
    async def dice(self, ctx: commands.context.Context, *parameters: tuple) -> None:
        """
        Throws a dice.
        By default, the dice has 6 sides, but you can change the number of sides writing the number as input.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `parameters` (tuple): it's an optional parameter; it is the number of sides.

        Returns:
            `None`
        """        
        if not(await checkRole(ctx, AuthorizationLevelEnum.OSPITI)):
            return None
        number = -1
        if len(parameters) == 0:
            number = 6
        elif len(parameters) == 1:
            try:
                number = int(parameters[0])
            except:
                number = -1
        if number > 0:
            await ctx.send(randrange(number) + 1)
        else:
            embed = Embed(title='Comando non corretto', description='Il comando può essere:', color=0xffd519)
            embed.set_author(name = 'RapaxBot', icon_url = 'https://cdn.discordapp.com/attachments/675275973918195712/924566156407341076/Logo_RAPAX_Cerchio.png')
            embed.add_field(name='`>dice`', value='Tira un dado a 6 facce.', inline=False)
            embed.add_field(name='`>dice x`', value='Tira un dado a `x` facce; `x` è un numero intero positivo.', inline=True)
            await ctx.send(embed=embed)

    @commands.command()
    async def coin(self, ctx: commands.context.Context) -> None:
        """
        Throws a coin.

        Args:
            `ctx` (commands.context.Context): it's the context.

        Returns:
            `None`
        """        
        if not(await checkRole(ctx, AuthorizationLevelEnum.OSPITI)):
            return None
        moneta = ['Testa', 'Croce']
        await ctx.send(choice(moneta))

    @commands.command()
    async def prison(self, ctx: commands.context.Context, member: Member, time: int, *, message: str) -> None:
        """
        Change temporarily the roles of the member passed as parameter.
        It removes all the roles and send him to the prison (if he's connected in a voice channel).
        After `time` seconds, it restore che member roles.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `member` (Member): the member whose go to the prison.
            `time` (int): the time in second.
            `message` (str): the motivation.

        Returns:
            `None`
        """        
        if not(await checkRole(ctx, AuthorizationLevelEnum.UFFICIALE)):
            return None
        guild = ctx.guild
        channel_text_prison = guild.get_channel(CH_TXT_PRIGIONE)
        channel_voice_prison = guild.get_channel(CH_VCL_PRIGIONE_VOCALE)
        role = guild.get_role(AMMINISTRATORE)
        list_roles = member.roles
        # Remove from the "to remove role list" administrator role
        if role in list_roles:
            list_roles.remove(role)
        role = guild.get_role(PRIGIONIERO)
        # Check if the member already has prisoner role
        if role in list_roles:
            await ctx.send('È già prigionero')
            return None
        # Remove the member's roles and add the prisoner role
        for i in range(1, len(list_roles)):
            await member.remove_roles(list_roles[i])
        await member.add_roles(role)
        # Move the member to prison voice chat
        try:
            member.voice.channel != None
            channel_voice = member.voice.channel
            await member.move_to(channel_voice_prison)
        except:
            pass
        # Send ack
        await channel_text_prison.send(member.display_name + ' è stato messo in prigione per ' + str(time) + ' secondi.\nMotivazione: ' + message)
        # Wait
        await asyncio.sleep(time)
        # Restore member's rols
        for i in range(1, len(list_roles)):
            await member.add_roles(list_roles[i])
        await member.remove_roles(role)
        # Move the member to the voice chat where he was before he was moved
        try:
            await member.move_to(channel_voice)
        except:
            pass
        # Send ack
        await channel_text_prison.send(member.display_name + ' ha scontato la propria pena. Fine della quarantena.')

    @commands.command()
    async def torp(self, ctx: commands.context.Context, member: Member) -> None:
        """
        Add temporarily the roles 'torpedo-friend' role to the member passed as parameter.
        After 5 minutes, it removes the role.

        Args:
            `ctx` (commands.context.Context): it's the context.
            `member` (Member): the member whose became 'torpedo-friend'.

        Returns:
            `None`
        """        
        if not(await checkRole(ctx, AuthorizationLevelEnum.MEMBRO_DEL_CLAN)):
            return None
        guild = ctx.guild
        channel = guild.get_channel(CH_TXT_PRIGIONE)
        role = guild.get_role(TORPAMICI)
        list_roles = member.roles
        # Check if the member already has the torpedo-friend role
        if role in list_roles:
            await ctx.send('È già un torpamico')
            return None
        # Add the role
        await member.add_roles(role)
        # Send ack
        await channel.send(member.name + ' è diventato un torpamico per 5 minuti.')
        # Sleep
        await asyncio.sleep(300)
        # Remove the role
        await member.remove_roles(role)
        # Send ack
        await channel.send(member.name + ' non è più torpamico.')

def setup(bot):
    bot.add_cog(Entertainment(bot))
