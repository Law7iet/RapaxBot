from disnake import TextInputStyle, Role, TextChannel, ModalInteraction, ui, Embed

from utils.functions import send_response_and_clear


class Modal(ui.Modal):
    def __init__(self, role: Role, channel: TextChannel, message: str = None):
        self.role = role
        self.channel = channel
        self.message_id = message
        components = [
            ui.TextInput(
                label="Titolo",
                placeholder="Inserisci qua il titolo.",
                custom_id="title",
                style=TextInputStyle.short,
                required=False
            ),
            ui.TextInput(
                label="Testo",
                placeholder="Inserisci qua il messaggio.",
                custom_id="description",
                style=TextInputStyle.paragraph,
                required=not self.message_id
            )
        ]
        super().__init__(
            title="Modal",
            custom_id="modal",
            components=components
        )

    async def callback(self, inter: ModalInteraction):
        try:
            if self.message_id is None:
                embed = Embed(
                    title=inter.text_values["title"],
                    description=inter.text_values["description"],
                    color=0xffd519
                )
                await self.channel.send("<@&" + str(self.role.id) + ">", embed=embed)
            else:
                message = await self.channel.fetch_message(int(self.message_id))
                old_embed = message.embeds[0]
                embed = Embed(
                    title=old_embed.title if inter.text_values["title"] == "" else inter.text_values["title"],
                    description=old_embed.description if inter.text_values["description"] == "" else inter.text_values["description"],
                    color=0xffd519
                )
                await message.edit(content="<@&" + str(self.role.id) + ">", embed=embed)
            await send_response_and_clear(inter, "Fatto!")

        except AttributeError:
            await send_response_and_clear(inter, "Messaggio non trovato.")
        except ValueError:
            await send_response_and_clear(inter, "ID del messaggio non corretto.")
        except Exception as error:
            await inter.response.send_message("Errore durante la generazione del modal.\n" + str(error))
