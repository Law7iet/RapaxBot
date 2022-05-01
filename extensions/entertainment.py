import asyncio
from random import choice
from random import randrange, random

from disnake import ApplicationCommandInteraction, Embed, Member
from disnake.ext import commands

from utils.constants import *
from utils.functions import *

VoteOptions = commands.option_enum({
    "Default": "Default",
    "Reddit": "Reddit"
})


class Entertainment(commands.Cog):
    def __init__(self, bot: commands.Cog):
        self.bot = bot

    @commands.slash_command(
        name="ping",
        description="Ping pong!"
    )
    async def ping(self, inter: ApplicationCommandInteraction) -> None:
        """
        A simple command that responses with "Pong!".

        Args:
            inter: it's the application command interation (context).
        
        Returns:
            None
        """
        await inter.response.send_message("Pong!")

    @commands.slash_command(
        name="Vote",
        description="Manda un messaggio con le reazioni per poter votare il messaggio."
    )
    async def vote(self, inter: ApplicationCommandInteraction, tipo: VoteOptions, messaggio: str) -> None:
        """
        Add 3 reactions to the message; the reactions are \U00002705, \U0000274C, and \U00002753.
        If the message's author is the person who called this command, it adds the emojis if the caller is at least an
        executive officer.

        Args:
            messaggio: the message that you want to add the reactions.
            tipo: the type of the reactions.
            inter:

        Returns:
            None
        """
        await inter.response.send_message(messaggio)
        message = await inter.original_message()
        match tipo:
            case "Default":
                emojis = ["\U00002705", "\U0000274C"]
            case "Reddit":
                emojis = ["<:upvote:963800988211355648>", "<:downvote:963801020725612584>"]
            case _:
                return
        for emoji in emojis:
            await message.add_reaction(emoji)

    @commands.slash_command(
        name="vote_message",
        description="Aggiunge al messaggio passato per ID le reazioni per votare."
    )
    async def vote_message(self, inter: ApplicationCommandInteraction, tipo: VoteOptions, id_canale: str, id_messaggio: str) -> None:
        """
        Add 3 reactions to the message; the reactions are \U00002705, \U0000274C, and \U00002753.
        If the message's author is the person who called this command, it adds the emojis if the caller is at least an
        executive officer.

        Args:
            messaggio: the message that you want to add the reactions.
            tipo: the type of the reactions.
            inter:

        Returns:
            None
        """
        author = inter.author
        guild = inter.guild
        try:
            channel = guild.get_channel(int(id_canale))
            msg = await channel.fetch_message(int(id_messaggio))
        except:
            await inter.response.send_message("Messaggio/canale non trovato.")
            await asyncio.sleep(5)
            message = await inter.original_message()
            await message.delete()
            return None
        if msg.author != author:
            if not (await check_role(inter, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
                await inter.response.send_message("Non hai i permessi.")
                await asyncio.sleep(5)
                message = await inter.original_message()
                await message.delete()
                return None
        match tipo:
            case "Default":
                emojis = ["\U00002705", "\U0000274C"]
            case "Reddit":
                emojis = ["<:upvote:963800988211355648>", "<:downvote:963801020725612584>"]
            case _:
                return
        for emoji in emojis:
            await msg.add_reaction(emoji)
        await inter.response.send_message("Fatto!")
        await asyncio.sleep(5)
        message = await inter.original_message()
        await message.delete()

    @commands.slash_command(
        name="dice",
        description="Tira un dado con n facce. Di default n è 6"
    )
    async def dice(self, inter: ApplicationCommandInteraction, n: int = 6) -> None:
        """
        Throws a die.
        By default, the dice has 6 sides, but you can change the number of sides writing the number than input.

        Args:
            ctx: it's the context.
            parameters: it's an optional parameter; it is the number of sides.

        Returns:
            None
        """
        if not (await check_role(inter, AuthorizationLevelEnum.OSPITI)):
            await inter.response.send_message("Non hai i permessi.")
            await asyncio.sleep(5)
            message = await inter.original_message()
            await message.delete()
            return None
        await inter.response.send_message("Risultato del dado a " + str(n) + " facce: **" + str(randrange(n) + 1) + "**")

    @commands.slash_command(
        name="coin",
        description="Lancia una moneta. Potrebbe cadere in piedi"
    )
    async def coin(self, inter: ApplicationCommandInteraction) -> None:
        """
        Throws a coin.

        Args:
            ctx: it's the context.

        Returns:
            None
        """
        if not (await check_role(inter, AuthorizationLevelEnum.OSPITI)):
            await inter.response.send_message("Non hai i permessi.")
            await asyncio.sleep(5)
            message = await inter.original_message()
            await message.delete()
            return None
        x = random()
        if x > 0.5:
            moneta = "Testa"
        elif x < 0.5:
            moneta = "Croce"
        else:
            await inter.response.send_message("@everyone la moneta è caduta in piedi!")
        await inter.response.send_message("È uscito " + moneta)

    @commands.command()
    async def prison(self, ctx: commands.context.Context, member: Member, time: int, *, message: str) -> None:
        """
        Change temporarily the roles of the member passed as parameter.
        It removes all the roles and send him to the prison (if he's connected in a voice channel).
        After `time` seconds, it restore che member roles.

        Args:
            ctx: it's the context.
            member: the member whose go to the prison.
            time: the time in second.
            message: the motivation.

        Returns:
            None
        """
        if not (await check_role(ctx, AuthorizationLevelEnum.UFFICIALE)):
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
            if member.voice.channel is not None:
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
            ctx: it's the context.
            member: the member whose became 'torpedo-friend'.

        Returns:
            None
        """
        if not (await check_role(ctx, AuthorizationLevelEnum.MEMBRO_DEL_CLAN)):
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
