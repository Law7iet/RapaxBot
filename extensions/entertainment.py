from random import randrange, random, sample

from disnake import Member, TextChannel
from disnake.ext import commands

from utils.constants import AuthorizationLevelEnum, CH_TXT_PRIGIONE, CH_VCL_PRIGIONE_VOCALE, AMMINISTRATORE, PRIGIONIERO, TORPAMICI
from utils.functions import *
from utils.apiWargaming import ApiWargaming

VoteStyleOptions = commands.option_enum({
    "Default": "Default",
    "Reddit": "Reddit"
})


def get_emoji_style(style: VoteStyleOptions) -> list[str]:
    match style:
        case "Default":
            return ["\U00002705", "\U0000274C"]
        case "Reddit":
            return ["<:upvote:963800988211355648>", "<:downvote:963801020725612584>"]
        case _:
            return []


TierOptions = commands.option_enum({
    "All": "All",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "10": "10",
    "11": "11",
})

ShipTypeOptions = commands.option_enum({
    "All": "All",
    "Destroyer": "Destroyer",
    "Cruiser": "Cruiser",
    "Battleship": "Battleship",
    "Aircraft Carrier": "AirCarrier"
    # "Submarine": "Submarine"
})


class Entertainment(commands.Cog):
    def __init__(self, bot: commands.Cog):
        self.bot = bot
        self.apiWargaming = ApiWargaming()

    @commands.slash_command()
    async def vota(self, inter: ApplicationCommandInteraction) -> None:
        pass

    @vota.sub_command(description="Aggiunge le reazioni per poter votare uno specifico messaggio.")
    async def messaggio(
            self,
            inter: ApplicationCommandInteraction,
            stile: VoteStyleOptions,
            canale: TextChannel,
            id_messaggio: str
    ) -> None:
        """
        Add 2 reactions to the message's ID that matches with `messaggio`; there are two types of reactions: standard
        and reddit style. If the message's author is the person who called this command, it adds the emojis if the
        caller has at least the `executive officer` role.

        Args:
            inter: the application command interation (context).
            stile: the style of the reactions.
            canale: the channel where the message is.
            id_messaggio: the message's ID that you want to add the reactions.

        Returns:
            None
        """
        author = inter.author
        try:
            msg = await canale.fetch_message(int(id_messaggio))
        except AttributeError:
            await send_response_and_clear(inter, False, "Messaggio non trovato.")
            return
        except ValueError:
            await send_response_and_clear(inter, False, "ID del messaggio non corretto.")
            return
        if msg.author != author:
            if not (await check_role(inter, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
                await send_response_and_clear(inter, False, "Non hai i permessi.")
                return
        emojis = get_emoji_style(stile)
        for emoji in emojis:
            await msg.add_reaction(emoji)
        await send_response_and_clear(inter, False, "Fatto!")
        return

    @commands.slash_command(description="Tira un dado con n facce. Di default n è 6.")
    async def dice(self, inter: ApplicationCommandInteraction, n: int = 6) -> None:
        """
        Throws a die.
        By default, the dice has 6 sides, but you can change the number of sides writing the number than input.

        Args:
            inter: the application command interation (context).
            n: an optional parameter that states the number of the die's sides.

        Returns:
            None
        """
        if not (await check_role(inter, AuthorizationLevelEnum.OSPITI)):
            await send_response_and_clear(inter, False, "Non hai i permessi.")
            return
        await inter.response.send_message("Risultato del dado a " + str(n) + " facce: **" + str(randrange(n) + 1) +
                                          "**")

    @commands.slash_command(description="Lancia una moneta. Potrebbe cadere in piedi!")
    async def coin(self, inter: ApplicationCommandInteraction) -> None:
        """
        Throws a coin.

        Args:
            inter: the application command interation (context).

        Returns:
            None
        """
        if not (await check_role(inter, AuthorizationLevelEnum.OSPITI)):
            await send_response_and_clear(inter, False, "Non hai i permessi.")
            return
        x = random()
        if x > 0.5:
            message = "È uscito Testa"
        elif x < 0.5:
            message = "È uscito Croce"
        else:
            message = "@everyone la moneta è caduta in piedi!"
        await inter.response.send_message(message)

    @commands.slash_command(description="Mette in prigione un membro del clan per alcuni secondi.")
    async def imprigiona(
            self,
            inter: ApplicationCommandInteraction,
            chi: Member,
            secondi: int,
            *,
            motivazione: str = ""
    ) -> None:
        """
        Change temporarily the roles of the member passed as parameter.
        It removes all the roles and send him to the prison (if he's connected in a voice channel).
        After `secondi` seconds, it restores che member roles.

        Args:
            inter: the application command interation (context).
            chi: the member who goes to the prison.
            secondi: the time in second.
            motivazione: the motivation.

        Returns:
            None
        """
        if not (await check_role(inter, AuthorizationLevelEnum.UFFICIALE)):
            await send_response_and_clear(inter, False, "Non hai i permessi.")
            return
        guild = inter.guild
        channel_text_prison = guild.get_channel(CH_TXT_PRIGIONE)
        channel_voice_prison = guild.get_channel(CH_VCL_PRIGIONE_VOCALE)
        role = guild.get_role(AMMINISTRATORE)
        list_roles = chi.roles
        # Remove from the "to remove role list" administrator role
        if role in list_roles:
            list_roles.remove(role)
        role = guild.get_role(PRIGIONIERO)
        # Check if the member already has prisoner role
        if role in list_roles:
            await send_response_and_clear(inter, False, "È già un prigionero.")
            return
        # Remove the member's roles and add the prisoner role
        for i in range(1, len(list_roles)):
            await chi.remove_roles(list_roles[i])
        await chi.add_roles(role)
        # Move the member to prison voice chat
        try:
            if chi.voice.channel is not None:
                channel_voice = chi.voice.channel
                await chi.move_to(channel_voice_prison)
        except:
            pass
        # Send ack
        if motivazione:
            motivazione = "\nMotivazione: " + motivazione
        await channel_text_prison.send(chi.display_name + " è stato messo in prigione per " + str(secondi) +
                                       " secondi." + motivazione)
        await send_response_and_clear(inter, False, "Fatto!")
        # Wait
        await asyncio.sleep(secondi)
        # Restore member's roles
        for i in range(1, len(list_roles)):
            await chi.add_roles(list_roles[i])
        await chi.remove_roles(role)
        # Move the member to the voice chat where he was before he was moved
        try:
            await chi.move_to(channel_voice)
        except:
            pass
        # Send ack
        await channel_text_prison.send(chi.display_name + " ha scontato la propria pena. Fine della quarantena.")

    @commands.slash_command(description="Mette il ruolo torpamico per 5 minuti.")
    async def torpamico(self, inter: ApplicationCommandInteraction, chi: Member) -> None:
        """
        Add temporarily the roles 'torpedo-friend' role to the member passed as parameter.
        After 5 minutes, it removes the role.

        Args:
            inter: the application command interation (context).
            chi: the member whose became 'torpedo-friend'.

        Returns:
            None
        """
        if not (await check_role(inter, AuthorizationLevelEnum.MEMBRO_DEL_CLAN)):
            await send_response_and_clear(inter, False, "Non hai i permessi.")
            return
        guild = inter.guild
        channel = guild.get_channel(CH_TXT_PRIGIONE)
        role = guild.get_role(TORPAMICI)
        list_roles = chi.roles
        # Check if the member already has the torpedo-friend role
        if role in list_roles:
            await send_response_and_clear(inter, False, "È già un torpamico")
            return None
        # Add the role
        await chi.add_roles(role)
        # Send ack
        await channel.send(chi.name + ' è diventato un torpamico per 5 minuti.')
        await send_response_and_clear(inter, False, "Fatto!")
        # Sleep
        await asyncio.sleep(300)
        # Remove the role
        await chi.remove_roles(role)
        # Send ack
        await channel.send(chi.name + ' non è più torpamico.')

    @commands.slash_command(description="Sceglie alcune navi a caso di un giocatore.")
    async def randomize(self, inter: ApplicationCommandInteraction, giocatore: str, tipo: ShipTypeOptions,
                        tier: TierOptions) -> None:
        await inter.response.defer()
        found_player = self.apiWargaming.get_player_by_nick(giocatore)
        if not found_player:
            await send_response_and_clear(inter, True, "Giocatore non trovato")
        else:
            player_id = found_player[0]
            player_ships_id = self.apiWargaming.get_player_ships(player_id)
            if not player_ships_id:
                await send_response_and_clear(inter, True, "Giocatore non ha navi o ha l'account privato")
            else:
                player_mapped_ships = [
                    {
                        "Destroyer": list(),
                        "Cruiser": list(),
                        "Battleship": list(),
                        "AirCarrier": list()
                    },
                    {
                        "Destroyer": list(),
                        "Cruiser": list(),
                        "Battleship": list(),
                        "AirCarrier": list()
                    },
                    {
                        "Destroyer": list(),
                        "Cruiser": list(),
                        "Battleship": list(),
                        "AirCarrier": list()
                    },
                    {
                        "Destroyer": list(),
                        "Cruiser": list(),
                        "Battleship": list(),
                        "AirCarrier": list()
                    },
                    {
                        "Destroyer": list(),
                        "Cruiser": list(),
                        "Battleship": list(),
                        "AirCarrier": list()
                    },
                    {
                        "Destroyer": list(),
                        "Cruiser": list(),
                        "Battleship": list(),
                        "AirCarrier": list()
                    },
                    {
                        "Destroyer": list(),
                        "Cruiser": list(),
                        "Battleship": list(),
                        "AirCarrier": list()
                    },
                    {
                        "Destroyer": list(),
                        "Cruiser": list(),
                        "Battleship": list(),
                        "AirCarrier": list()
                    },
                    {
                        "Destroyer": list(),
                        "Cruiser": list(),
                        "Battleship": list(),
                        "AirCarrier": list()
                    },
                    {
                        "Destroyer": list(),
                        "Cruiser": list(),
                        "Battleship": list(),
                        "AirCarrier": list()
                    },
                    {
                        "Destroyer": list(),
                        "Cruiser": list(),
                        "Battleship": list(),
                        "AirCarrier": list()
                    }
                ]

                while len(player_ships_id) > 0:
                    num = len(player_ships_id) if len(player_ships_id) < 100 else 100
                    iteration = 0
                    query = ""
                    while iteration < num:
                        iteration = iteration + 1
                        ship_id = player_ships_id.pop(0)
                        query = query + str(ship_id) + "%2C+"
                    query = query[:-4]

                    res_data = await self.apiWargaming.get_ships_tier_and_name(query, tipo)
                    if res_data is None:
                        print("sus")
                        return
                    for key in res_data.keys():
                        if res_data[key] is None:
                            continue
                        else:
                            ship = res_data[key]
                            if ship["name"][0] == "[" and ship["name"][-1] == "]":
                                continue
                            if tipo == "All":
                                player_mapped_ships[ship["tier"] - 1][ship["type"]].append(ship["name"])
                            else:
                                player_mapped_ships[ship["tier"] - 1][tipo].append(ship["name"])

                # Print ships
                ships_pool = []
                for index in range(0, len(player_mapped_ships)):
                    if tier == "All" or int(tier) == index + 1:
                        for key in player_mapped_ships[index].keys():
                            if tipo == "All" or tipo == key:
                                ships_pool = ships_pool + player_mapped_ships[index][key]
                if len(ships_pool) == 0:
                    await send_response_and_clear(inter, True,
                                                  "Nessuna nave trovata di tipo " + tipo + " al tier " + tier)
                else:
                    ships = sample(ships_pool, 5 if len(ships_pool) >= 5 else len(ships_pool))
                    message = "Giocatore: `" + giocatore + "`\nTipologia di nave: `" + tipo + "`\nTier: `" + tier + "`\n" + ", ".join(
                        ships)
                    await inter.send(message)


def setup(bot):
    bot.add_cog(Entertainment(bot))
