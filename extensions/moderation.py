import re

from disnake import Embed, Role, TextChannel, errors, ApplicationCommandInteraction
from disnake.ext import commands

from utils.constants import OSPITI, CH_TXT_TESTING, CH_TXT_CALENDARIO, AuthorizationLevelEnum, DEBUG
from utils.functions import send_response_and_clear, check_role

from utils.modal import Modal

EventOptions = commands.option_enum({
    "Clan Battle": "Clan Battle",
    "Allenamento": "allenamento"
})


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Cog):
        self.bot = bot

    async def presenze(
        self,
        inter: ApplicationCommandInteraction,
        evento: EventOptions,
        ruolo: Role,
        messaggio: str,
        keys: list[str],
        reactions: list[str],
        icon: str
    ):
        if not (await check_role(inter, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            await send_response_and_clear(inter, False, "Non hai i permessi.")
            return
        if DEBUG:
            channel = self.bot.get_channel(CH_TXT_TESTING)
            ping = "<@&" + str(OSPITI) + ">"
        else:
            channel = self.bot.get_channel(CH_TXT_CALENDARIO)
            ping = "<@&" + str(ruolo.id) + ">"

        title = "Presenze " + evento
        embed = Embed(title=title, description=ping + "\n" + messaggio + "\n\n\n" + "\n".join(keys), color=0xffd519)
        embed.set_author(name="RapaxBot")
        embed.set_thumbnail(url=icon)

        msg = await channel.send(ping, embed=embed)
        for element in reactions:
            await msg.add_reaction(element)

        await send_response_and_clear(inter, True, "Fatto!")

    @commands.slash_command()
    async def scrivi(self, inter: ApplicationCommandInteraction) -> None:
        pass

    @scrivi.sub_command(description="Il bot scrive un messaggio per te.")
    async def messaggio(
        self,
        inter: ApplicationCommandInteraction,
        canale: TextChannel,
        ruolo: Role
    ) -> None:
        """
        Write an embed message using the bot profile. The message must tag a role and it must have a text. The title is
        optional

        Args:
            inter: the application command interation (context).
            canale: the channel where you want to send the message.
            ruolo: the role who will be pinged.

        Returns:
            None
        """
        if not (await check_role(inter, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            await send_response_and_clear(inter, False, "Non hai i permessi.")
            return
        await inter.response.send_modal(modal=Modal(ruolo, canale))

    @commands.slash_command()
    async def modifica(self, inter: ApplicationCommandInteraction) -> None:
        pass

    @modifica.sub_command(description="Modifica un messaggio-embed del bot.")
    async def messaggio(
        self,
        inter: ApplicationCommandInteraction,
        canale: TextChannel,
        id_messaggio: str,
        ruolo: Role
    ) -> None:
        """
        Edit the embed message. If in the modal the fields are empty, it doesn't edit the empty field.

        Args:
            inter: the application command interation (context).
            canale: the channel where you want to send the message.
            id_messaggio: the message's id.
            ruolo: the role who will be pinged.

        Returns:
            None
        """
        if not (await check_role(inter, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            await send_response_and_clear(inter, False, "Non hai i permessi.")
            return
        await inter.response.send_modal(modal=Modal(ruolo, canale, id_messaggio))

    @commands.slash_command()
    async def aggiungi(self, inter: ApplicationCommandInteraction) -> None:
        pass

    @aggiungi.sub_command(description="Aggiunge una reazione al messaggio indicato.")
    async def reazione(
        self,
        inter: ApplicationCommandInteraction,
        canale: TextChannel,
        id_messaggio: str,
        emoji: str
    ) -> None:
        """
        Add a reaction to a message. It works only for default's emoji and server's emoji.

        Args:
            inter: the application command interation (context).
            canale: the channel where you want to send the message.
            id_messaggio: the message's id.
            emoji: the emoji you want to use as reaction.

        Returns:
            None
        """
        if not (await check_role(inter, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            await send_response_and_clear(inter, False, "Non hai i permessi.")
            return
        try:
            message = await canale.fetch_message(int(id_messaggio))
            await message.add_reaction(emoji)
        except ValueError:
            await send_response_and_clear(inter, False, "ID del messaggio non corretto.")
            return
        except errors.HTTPException as error:
            match error.code:
                case 10008:
                    await send_response_and_clear(inter, False, "Messaggio non trovato.")
                    return
                case 10014:
                    await send_response_and_clear(inter, False, "Emoji non valido.")
                    return
                case _:
                    await send_response_and_clear(inter, False, "Errore generico.\n" + str(error))
                    return
        await send_response_and_clear(inter, False, "Fatto!")

    @commands.slash_command()
    async def presenza(self, inter: ApplicationCommandInteraction) -> None:
        pass

    @presenza.sub_command(description="Manda le presenze per un evento")
    async def giornaliera(
        self,
        inter: ApplicationCommandInteraction,
        evento: EventOptions,
        ruolo: Role,
        messaggio: str = ""
    ) -> None:
        """
        Generate the participation message for a specific Clan Battles or Training day.

        Args:
            inter: the application command interation (context).
            evento: the event.
            ruolo: the role who will be pinged.
            messaggio: the message.

        Returns:
            None
        """
        await inter.response.defer()
        match evento:
            case "Clan Battle":
                keys = [
                    "- \U00000031\U000020E3 19:00-21:00",
                    "- \U00000032\U000020E3 21:00-23:00",
                    "- \U0001F557 Arrivo tardi",
                    "- \U0000274C Non disponibile",
                    "- \U00002753 Forse"
                ]
                reactions = [
                    "\U00000031\U000020E3",
                    "\U00000032\U000020E3",
                    "\U0001F557",
                    "\U0000274C",
                    "\U00002753"
                ]
                icon = "https://cdn.discordapp.com/attachments/675275973918195712/951066454596419604/clanBattle.png"
            case "allenamento":
                keys = [
                    "- \U00002705 Presente",
                    "- \U0001F557 Arrivo tardi",
                    "- \U0000274C Assente",
                    "- \U00002753 Forse"
                ]
                reactions = [
                    "\U00002705",
                    "\U0001F557",
                    "\U0000274C",
                    "\U00002753"
                ]
                icon = "https://cdn.discordapp.com/attachments/675275973918195712/944964438652506192/training.png"
            case _:
                return
        await self.presenze(inter, evento, ruolo, messaggio, keys, reactions, icon)

    @presenza.sub_command(description="Richiede le presenze dei giocatori per una settimana.")
    async def settimanale(
        self,
        inter: ApplicationCommandInteraction,
        evento: EventOptions,
        ruolo: Role,
        messaggio: str = ""
    ) -> None:
        """
        Generate the participation message for the Clan Battles or Training.

        Args:
            inter: the application command interation (context).
            evento: the event.
            ruolo: the role who will be pinged.
            messaggio: the message.

        Returns:
            None
        """
        await inter.response.defer()
        match evento:
            case "Clan Battle":
                keys = [
                    "Mercoledì",
                    "- :one: 19:00-21:00",
                    "- :two: 21:00-23:00",
                    "Giovedì",
                    "- :three: 19:00-21:00",
                    "- :four: 21:00-23:00",
                    "Sabato",
                    "- :five: 19:00-21:00",
                    "- :six: 21:00-23:00",
                    "Domenica",
                    "- :seven: 19:00-21:00",
                    "- :eight: 21:00-23:00",
                ]
                reactions = [
                    "\U00000031\U000020E3",
                    "\U00000032\U000020E3",
                    "\U00000033\U000020E3",
                    "\U00000034\U000020E3",
                    "\U00000035\U000020E3",
                    "\U00000036\U000020E3",
                    "\U00000037\U000020E3",
                    "\U00000038\U000020E3"
                ]
                icon = "https://cdn.discordapp.com/attachments/675275973918195712/951066454596419604/clanBattle.png"
            case "allenamento":
                keys = [
                    "- :one: lunedì",
                    "- :two: martedì",
                    "- :three: mercoledì",
                    "- :four: giovedì",
                    "- :five: venerdì",
                    "- :six: sabato",
                    "- :seven: domenica"
                ]
                reactions = [
                    "\U00000031\U000020E3",
                    "\U00000032\U000020E3",
                    "\U00000033\U000020E3",
                    "\U00000034\U000020E3",
                    "\U00000035\U000020E3",
                    "\U00000036\U000020E3",
                    "\U00000037\U000020E3"
                ]
                icon = "https://cdn.discordapp.com/attachments/675275973918195712/944964438652506192/training.png"
            case _:
                return
        await self.presenze(inter, evento, ruolo, messaggio, keys, reactions, icon)


def setup(bot: commands.Cog):
    bot.add_cog(Moderation(bot))
