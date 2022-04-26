import re
from discord import Embed, Emoji
from discord.ext import commands
from utils.constants import *
from utils.functions import *
from utils.apiWarGaming import ApiWarGaming


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.apiWargaming = ApiWarGaming()

    async def presenze(self, ctx: commands.context.Context, event_type: WowsEventEnum, message: str) -> None:
        """
        Generate the participation message for Clan Battles, Clan Brawl, Training or other events.
        Each event is associated with the `WowsEventEnum` enum and each event has a own reaction.
        The keys are separated from the message by 3 new lines; using 3 new lines in a row you won't be able to edit the description.

        Args:
            ctx: it's the context.
            event_type: type of the event.
            message: the message which will be displayed in the embed as description.

        Returns:
            None
        """
        if not (await check_role(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None

        channel = self.bot.get_channel(CH_TXT_CALENDARIO)
        ping = "<@&" + str(MEMBRO_DEL_CLAN) + ">"
        # TEST MODE
        # channel = self.bot.get_channel(CH_TXT_TESTING)
        # ping = "<@&" + str(OSPITI) + ">"

        title = "Presenze " + wowsEvent[int(event_type)]
        if event_type == WowsEventEnum.CLAN_BATTLE:
            keys = CBKeys
            reactions = CBEmoji
            icon = "https://cdn.discordapp.com/attachments/675275973918195712/944874666164637736/clanBattle.png"
        elif event_type == WowsEventEnum.CLAN_BRAWL:
            keys = CBKeys
            reactions = CBEmoji
            icon = "https://cdn.discordapp.com/attachments/675275973918195712/944874666391142500/clanBrawl.png"
        elif event_type == WowsEventEnum.TRAINING:
            keys = eventKeys
            reactions = eventEmoji
            icon = "https://cdn.discordapp.com/attachments/675275973918195712/944964438652506192/training.png"
        elif event_type == WowsEventEnum.OTHER:
            keys = voteKeys
            reactions = voteEmoji
            icon = 'https://cdn.discordapp.com/attachments/675275973918195712/944988546811461653/rapax.png'
        else:
            return None
        embed = Embed(title=title, description=message + "\n\n\n" + "\n".join(keys), color=0xffd519)
        embed.set_author(name="RapaxBot")
        embed.set_thumbnail(url=icon)

        await channel.send(ping)
        msg = await channel.send(embed=embed)
        for element in reactions:
            await msg.add_reaction(element)

    @commands.command()
    async def edit_embed(self, ctx: commands.context.Context, channelId: int, messageId: int, *,
                         newDescription: str) -> None:
        """
        Edit the description of an embed message.
        The old description has one '3 new lines' to separe the own message and the keys. 

        Args:
            ctx: it's the context.
            channelId: the channel's ID where the message was sent.
            messageId: the message ID.
            newDescription: the new description of the embed.

        Returns:
            None
        """
        if not (await check_role(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
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
            await message.edit(embed=embed)
        except:
            return None

    @commands.command()
    async def write(self, ctx: commands.context.Context, channelId: int, *, message) -> None:
        """
        Write a message using the bot profile.

        Args:
            ctx: it's the context.
            channelId: the channel's ID where you want to write.
            message: the message you want to write.

        Returns:
            None
        """
        if not (await check_role(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None
        guild = ctx.guild
        channel = guild.get_channel(channelId)
        await channel.send(message)

    @commands.command()
    async def edit(self, ctx: commands.context.Context, channelId: int, messageId: int, *, newMessage: str) -> None:
        """
        Edit a message sent by the bot.

        Args:
            ctx: it's the context.
            channelId: the channel's ID where the message was sent.
            messageId: the message ID.
            newMessage: the new message.

        Returns:
            None
        """
        if not (await check_role(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None
        guild = ctx.guild
        channel = guild.get_channel(channelId)
        message = await channel.fetch_message(messageId)
        await message.edit(content=newMessage)

    @commands.command()
    async def add_emoji(self, ctx: commands.context.Context, channel_id: int, message_id: int, emoji: Emoji) -> None:
        """
        Add a reaction to a message. It works only for default's emoji and server's emoji.

        Args:
            ctx: it's the context.
            channel_id: the channel's ID where the message was sent.
            message_id: the message ID which you want to add a reaction.
            emoji (Emoji): the emoji you want to use as reaction.

        Returns:
            None
        """
        if not (await check_role(ctx, AuthorizationLevelEnum.UFFICIALE_ESECUTIVO)):
            return None
        channel = ctx.message.channel
        await ctx.message.delete()
        message = await channel.fetch_message(message_id)
        await message.add_reaction(emoji)

    @commands.command()
    async def CB(self, ctx: commands.context.Context, *, message: str) -> None:
        """
        Sent an embed that requests the partecipation of the Clan Battle.

        Args:
            ctx: it's the context.
            message: it's the message that compares in the embed as description.

        Returns:
            None
        """
        await self.presenze(ctx, WowsEventEnum.CLAN_BATTLE, message)

    @commands.command()
    async def cb(self, ctx: commands.context.Context, *, message: str) -> None:
        """
        Sent an embed that requests the partecipation of the Clan Brawl.

        Args:
            ctx: it's the context.
            message: it's the message that compares in the embed as description.
        
        Returns:
            None
        """
        await self.presenze(ctx, WowsEventEnum.CLAN_BRAWL, message)

    @commands.command()
    async def training(self, ctx: commands.context.Context, *, message: str) -> None:
        """
        Sent an embed that requests the partecipation of the training.

        Args:
            ctx: it's the context.
            message: it's the message that compares in the embed as description.
        
        Returns:
            None
        """
        await self.presenze(ctx, WowsEventEnum.TRAINING, message)

    @commands.command()
    async def event(self, ctx: commands.context.Context, *, message: str) -> None:
        """
        Sent an embed that requests the partecipation of a event.

        Args:
            ctx: it's the context.
            message: it's the message that compares in the embed as description.

        Returns:
            None
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
            ctx: it's the context.
        
        Returns:
            None
        """
        if not (await check_role(ctx, AuthorizationLevelEnum.AMMINISTRATORE)):
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
                    player_info = self.apiWargaming.get_player_by_nick(userCurrentNickname)
                    if player_info is None:
                        await ctx.send("\U000026A0 Il membro `" + member.display_name + "` non è stato trovato.")
                        continue
                    # search tag with WoWs API
                    clan_id = self.apiWargaming.get_clan_by_player_id(player_info[0])

                    # DEBUG
                    # print(user_current_nickname + ": " + str(clan_id))

                    if clan_id is None:
                        # The player has not a clan
                        pass
                    else:
                        # The player has a clan
                        # Check if the role exists, else create it
                        clan_info = self.apiWargaming.get_clan_name_by_id(clan_id)
                        if get(guild.roles, name=clan_info[0]) is None:
                            await guild.create_role(name=clan_info[0], hoist=True, reason='Tag del Clan')
                            await ctx.send("\U0001F464 nuovo tag: `" + clan_info[0] + "`")
                        # Change user tag
                        if clan_info[1] != user_current_tag:
                            user_current_tag = clan_info[1]
                            await ctx.send(
                                "\U00002705 `" + member.display_name + "` cambiato tag `" + clan_info[1] + "`")
                        # Change user role
                        # TO-DO: Compute and remove the old role
                        # Add the role
                        clan_role = get(guild.roles, name=clan_info[0])
                        if not (clan_role in member.roles):
                            await member.add_roles(clan_role, reason="Clan Tag")
                            await ctx.send(
                                "\U00002705 `" + member.display_name + "` aggiunto il ruolo `" + clan_role.name + "`")

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

    @commands.command()
    async def rules(self, ctx):
        channel = self.bot.get_channel(722220184814747678)
        await channel.send(
            "**REGOLAMENTO**\n Le regole sono divise in 3 sezioni; le prime due descrivono le regole generali che tutti gli utenti all’interno del server devono seguire, mentre la terza parte regolamenta i comportamenti che ogni membro del clan deve mantenere.")
        embed = Embed(title="Sezione 1 - Moralità del Clan",
                      description="Un clan è essenzialmente composto da persone che, legate da un’attività in comune, dedicano parte del tempo per divertirsi insieme. Al fine di creare un luogo sereno, gli amministratori del server hanno il dovere di allontanare bandendo le persone che non rispettano i seguenti articoli.",
                      color=0x710d0f)
        embed.add_field(name="1.1", value="Rispettare tutte le persone all'interno di questo server.", inline=False)
        embed.add_field(name="1.2", value="Essere educati o adottare un comportamento non violento o discriminatorio.",
                        inline=False)
        embed.add_field(name="1.3", value="Evitare discussioni aventi temi religiosi, razziali e politici.",
                        inline=False)
        embed.add_field(name="1.4",
                        value="Sono ammessi comportamenti apertamente ironici, sempre nel limite del rispetto degli altri individui.",
                        inline=False)
        await channel.send(embed=embed)

        embed = Embed(title="Sezione 2 - Il server",
                      description="Il clan RAPAX si basa principalmente su Discord, cercando di sfruttare tutte le funzionalità di tale servizio di messaggistica. Per tale ragione è obbligatorio, pena l\’espulsione dal server, rispettare i seguenti articoli.",
                      color=0xb85513)
        embed.add_field(name="2.1",
                        value="Il nickname di ogni giocatore all\’interno del server deve essere cambiato con `[clan tag] nickname (nome)`.",
                        inline=False)
        embed.add_field(name="2.1.1",
                        value="Ogni utente è responsabile del proprio nickname: cambiando nickname o clan, sarà dovere suo cambiare il proprio nickname. È possibile che gli amministratori del server, attraverso un sistema automatizzato cambino il vostro nickname.",
                        inline=False)
        embed.add_field(name="2.2",
                        value="Non menzionare le persone o gruppi di persone con troppa frequenza utilizzando il comando `@user/role`.",
                        inline=False)
        embed.add_field(name="2.3",
                        value="Rispettare i topic dei canali testuali e vocali. L'argomento di ogni canale testuale è descritto in alto vicino al nome del canale. Per ogni canale è consigliato visionare i messaggi allegati.",
                        inline=False)
        await channel.send(embed=embed)

        embed = Embed(title="Sezione 3 - Il clan RAPAX & GEMINA",
                      description="La frequenza degli eventi del clan costituisce elemento fondante per l’aggregazione e lo sviluppo del clan stesso. Il mancato rispetto delle seguenti regole comporta l’espulsione dal clan.",
                      color=0xffd519)
        embed.add_field(name="3.1",
                        value="L’uso di Discord per la comunicazione tra i membri del clan è obbligatoria, non è un’opzione.",
                        inline=False)
        embed.add_field(name="3.1.1",
                        value="È fortemente consigliato utilizzare i canali vocali all’interno del server quando si sta giocando a World of Warships.",
                        inline=False)
        embed.add_field(name="3.1.2",
                        value="Tutte le comunicazioni principali avvengono in <#680757461606727710>. È obbligatorio aggiornarsi sulle novità del clan tramite quel canale e interagire ai messaggi con le opportune reazioni laddove è richiesto.",
                        inline=False)

        embed.add_field(name="3.2",
                        value="Partecipare agli allenamenti del clan. La partecipazione agli allenamenti è elemento necessario ma non sufficiente per poter partecipare agli eventi competitivi del clan.",
                        inline=False)
        embed.add_field(name="3.3", value="Partecipare alle Clan Battles e ai tornei vari.", inline=False)
        embed.add_field(name="3.3.1",
                        value="La partecipazione ai vari eventi è accessibile a tutti i membri salvo che il clan non decida di partecipare competitivamente.",
                        inline=False)
        embed.add_field(name="3.3.2",
                        value="Durante tali attività, bisogna seguire gli ordini dei propri superiori. Se si crede che l’ordine sia errato, la contestazione deve avvenire in un momento tranquillo; è indispensabile l’aspetto critico nella discussione.",
                        inline=False)

        embed.add_field(name="3.4", value="Partecipare attivamente alle battaglie navali ogni weekend.", inline=False)
        embed.add_field(name="3.5",
                        value="I membri devono essere attivi almeno una volta ogni tre settimane, ossia l’indicatore *Last Battle Time* non deve superare i 21 giorni.",
                        inline=False)
        embed.add_field(name="3.6",
                        value="Sono ammesse giustificazioni ragionevoli dalla mancata partecipazione alla vita del clan. È possibile che una prolungata assenza generi l’allontanamento dell’individuo dal clan.",
                        inline=False)
        embed.set_footer(
            text="Se gli amministratori ritengono necessario, in casi eccezionali tali regole possono essere non applicate. Si riserva sempre agli amministratori la possibilità di modificare tali regole per migliorare la qualità del clan.")
        await channel.send(embed=embed)

        await channel.send("Link al server **Legio XXI - RAPAX**: https://discord.gg/jxyrQ9C")


def setup(bot: commands.Cog):
    bot.add_cog(Moderation(bot))
