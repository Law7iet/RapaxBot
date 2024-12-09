from disnake import Role, TextChannel, errors, ApplicationCommandInteraction
from disnake.ext import commands

from utils.constants import AuthorizationLevelEnum
from utils.functions import send_response_and_clear, check_role

from utils.modal import Modal


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Cog):
        self.bot = bot

    @commands.slash_command()
    async def scrivi(self, inter: ApplicationCommandInteraction) -> None:
        pass

    @scrivi.sub_command(description="Il bot scrive un messaggio per te.")
    async def comunicazione(
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
        if not await check_role(inter, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO):
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
        if not await check_role(inter, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO):
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
        if not await check_role(inter, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO):
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


def setup(bot: commands.Cog):
    bot.add_cog(Moderation(bot))
