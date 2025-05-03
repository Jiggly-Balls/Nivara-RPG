from __future__ import annotations

import datetime
import random
from typing import TYPE_CHECKING

import discord
from discord import Embed

from backend.cache import Cache
from core.utils import ErrorEmbed, MainEmbed
from data.constants.core import PRIMARY_COLOUR
from data.constants.games import (
    ROULETTE_KILL_TEXTS,
    ROULETTE_MISS_TEXTS,
    ROULETTE_SUICIDE_KILL_TEXTS,
    ROULETTE_SUICIDE_MISS_TEXTS,
    Direction,
)
from data.games.mine import MineEngine
from data.games.roulette import ChamberIterator, PlayerIterator
from data.timeouts.views import ROULETTE_AUTOSTART

if TYPE_CHECKING:
    from discord import Button, Interaction, Member


class MineButton(discord.ui.Button["MineGameView"]):
    def __init__(self, emoji: str, direction: Direction) -> None:
        super().__init__(emoji=emoji, style=discord.ButtonStyle.blurple)

        self.direction = direction

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()

        if not interaction.user or not self.view or not interaction.message:
            return

        if interaction.user.id != self.view.author:
            await interaction.followup.send(
                embed=ErrorEmbed("This game is not for you."), ephemeral=True
            )
            return

        self.view.engine.move_player(self.direction)
        new_image = self.view.engine.create_image()
        await interaction.followup.edit_message(
            interaction.message.id, content=new_image
        )


class MineGameView(discord.ui.View):
    def __init__(self, author: int, engine: MineEngine) -> None:
        super().__init__(timeout=300, disable_on_timeout=True)

        self.author = author
        self.engine = engine

        self.add_item(MineButton(emoji="⬆", direction=Direction.UP))
        self.add_item(MineButton(emoji="⬇", direction=Direction.DOWN))
        self.add_item(MineButton(emoji="⬅", direction=Direction.LEFT))
        self.add_item(MineButton(emoji="➡", direction=Direction.RIGHT))


####


def roulette_embedder(guild: int, author: Member) -> Embed:
    countdown = Cache.roulette_active[guild]["countdown"]
    total_players = len(Cache.roulette_active[guild]["players"].player_list)
    player_list = "\n".join(
        [
            f"`{num}.` **{user.name}**"
            for num, user in enumerate(
                Cache.roulette_active[guild]["players"].player_list, start=1
            )
        ]
    )

    join_embed = Embed(
        description=f"Twisted Roulette has been initiated by {author.mention}.\nJoin the game by clicking on the button or from </game twisted_roulette join:1198957817248370688>",
        colour=PRIMARY_COLOUR,
    )

    join_embed.add_field(name="Game Auto-Starts", value=countdown)
    join_embed.add_field(
        name="Number of Players", value=f"{total_players} / 8", inline=False
    )
    join_embed.add_field(name="Players", value=player_list, inline=False)

    return join_embed


class RouletteButton(discord.ui.Button["RouletteGame"]):
    def __init__(self, player: discord.Member, guild: int) -> None:
        super().__init__(label=player.name, style=discord.ButtonStyle.green)
        self.player = player
        self.guild = guild

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        if (
            interaction.user
            in Cache.roulette_active[self.guild]["players"].dead_players
        ):
            await interaction.followup.send(
                embed=MainEmbed("You're dead!"), ephemeral=True
            )
            return

        elif (
            interaction.user
            not in Cache.roulette_active[self.guild]["players"].dead_players
            + Cache.roulette_active[self.guild]["players"].player_list
        ):
            await interaction.followup.send(
                embed=MainEmbed("You're not a part of the game."),
                ephemeral=True,
            )
            return

        elif (
            interaction.user
            != Cache.roulette_active[self.guild]["players"].current_player
        ):
            await interaction.followup.send(
                embed=MainEmbed("It is not your turn yet!"), ephemeral=True
            )
            return

        killer = Cache.roulette_active[self.guild]["players"].current_player
        next(Cache.roulette_active[self.guild]["chamber"])

        # The killer hit the shot -
        if Cache.roulette_active[self.guild]["chamber"].check_hit():
            self.disabled = True
            self.style = discord.ButtonStyle.red

            Cache.roulette_active[self.guild][
                "chamber"
            ].loaded_chamber = random.randint(1, 6)
            Cache.roulette_active[self.guild]["players"].kill(self.player)
            next(Cache.roulette_active[self.guild]["players"])
            new_player = Cache.roulette_active[self.guild][
                "players"
            ].current_player

            if self.player == killer:
                kill_text = random.choice(ROULETTE_SUICIDE_KILL_TEXTS).format(
                    self.player.mention
                )
            else:
                kill_text = random.choice(ROULETTE_KILL_TEXTS).format(
                    killer.mention, self.player.mention
                )

            killed_embed = MainEmbed(kill_text)

            if (
                len(Cache.roulette_active[self.guild]["players"].player_list)
                == 1
            ):
                self.view.disable_all_items()
                await interaction.followup.edit_message(
                    interaction.message.id,
                    content=None,
                    embeds=[
                        killed_embed,
                        MainEmbed(
                            f"GG {new_player.mention}! You have won the Twisted Roulette match!"
                        ),
                    ],
                    view=self.view,
                )
                del Cache.roulette_active[self.guild]

            else:
                await interaction.followup.edit_message(
                    interaction.message.id,
                    content=f"It's currently your turn {new_player.mention}",
                    embed=killed_embed,
                    view=self.view,
                )

        # The killer missed the shot -
        else:
            if (
                self.player
                != Cache.roulette_active[self.guild]["players"].current_player
            ):
                next(Cache.roulette_active[self.guild]["players"])

            if self.player == killer:
                kill_text = random.choice(ROULETTE_SUICIDE_MISS_TEXTS).format(
                    self.player.mention
                )
            else:
                kill_text = random.choice(ROULETTE_MISS_TEXTS).format(
                    killer.mention, self.player.mention
                )

            new_player = Cache.roulette_active[self.guild][
                "players"
            ].current_player
            await interaction.followup.edit_message(
                interaction.message.id,
                content=f"It's currently your turn {new_player.mention}",
                embed=MainEmbed(kill_text),
                view=self.view,
            )


class RouletteGame(discord.ui.View):
    def __init__(self, guild: int) -> None:
        super().__init__(timeout=None)

        for player in Cache.roulette_active[guild]["players"].player_list:
            self.add_item(RouletteButton(player=player, guild=guild))


class RouletteJoinView(discord.ui.View):
    def __init__(
        self,
        guild: int,
        author: discord.Member,
        message: discord.Message,
    ) -> None:
        super().__init__(timeout=ROULETTE_AUTOSTART)
        self.guild = guild
        self.author = author
        self.message = message
        self.countdown = Cache.roulette_active[guild]["countdown"]

    async def on_timeout(self) -> None:
        if self.guild in Cache.roulette_active:
            if (
                len(Cache.roulette_active[self.guild]["players"].player_list)
                < 2
                and not Cache.roulette_active[self.guild]["start"]
            ):
                del Cache.roulette_active[self.guild]
                return await self.message.edit(
                    embed=MainEmbed(
                        "Not enough players joined. The game was cancelled."
                    ),
                    view=None,
                )

            elif not Cache.roulette_active[self.guild]["start"]:
                self.disable_all_items()
                await self.message.edit(view=self)

                Cache.roulette_active[self.guild]["start"] = True
                first_player = Cache.roulette_active[self.guild][
                    "players"
                ].player_list[0]
                await self.message.channel.send(
                    f"It's currently your turn {first_player.mention}",
                    embed=MainEmbed("Click on whom you choose to kill."),
                    view=RouletteGame(guild=self.guild),
                )

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.blurple)
    async def start_game_callback(
        self, button: Button, interaction: Interaction
    ) -> None:
        await interaction.response.defer()
        if interaction.user.id != self.author.id:
            return await interaction.followup.send(
                embed=MainEmbed(
                    f"This game was initiated by {self.author.mention}. Hence only they can force start the game."
                ),
                ephemeral=True,
            )

        if (
            len(
                Cache.roulette_active[interaction.guild.id][
                    "players"
                ].player_list
            )
            < 2
        ):
            return await interaction.followup.send(
                embed=MainEmbed(
                    "A minimum of 2 players are required to start the game."
                ),
                ephemeral=True,
            )

        Cache.roulette_active[self.guild]["start"] = True

        await interaction.message.edit(
            embed=MainEmbed("The game has been initiated!"), view=None
        )

        first_player = Cache.roulette_active[self.guild][
            "players"
        ].player_list[0]
        await interaction.channel.send(
            f"It's currently your turn {first_player.mention}",
            embed=MainEmbed("Click on whom you choose to kill."),
            view=RouletteGame(guild=self.guild),
        )

    @discord.ui.button(label="Join Game", style=discord.ButtonStyle.blurple)
    async def join_game_callback(
        self, button: Button, interaction: Interaction
    ) -> None:
        await interaction.response.defer()
        if (
            interaction.user
            in Cache.roulette_active[interaction.guild.id][
                "players"
            ].player_list
        ):
            await interaction.followup.send(
                embed=MainEmbed("You're already a part of the game!"),
                ephemeral=True,
            )
            return

        Cache.roulette_active[interaction.guild.id][
            "players"
        ].player_list.append(interaction.user)
        await interaction.followup.send(
            embed=MainEmbed("You have joined the game!"), ephemeral=True
        )

        await self.message.edit(
            embed=roulette_embedder(self.guild, self.author)
        )

    @discord.ui.button(label="Leave Game", style=discord.ButtonStyle.red)
    async def leave_game_callback(
        self, button: Button, interaction: Interaction
    ) -> None:
        await interaction.response.defer()
        if (
            interaction.user
            not in Cache.roulette_active[interaction.guild.id][
                "players"
            ].player_list
        ):
            await interaction.followup.send(
                embed=MainEmbed("You're not a part of the game yet!"),
                ephemeral=True,
            )
            return

        Cache.roulette_active[interaction.guild.id][
            "players"
        ].player_list.remove(interaction.user)
        await interaction.followup.send(
            embed=MainEmbed("You have left the game!"), ephemeral=True
        )

        await self.message.edit(
            embed=roulette_embedder(self.guild, self.author)
        )


class RouletteInitView(discord.ui.View):
    def __init__(self, author: int) -> None:
        super().__init__(disable_on_timeout=True)
        self.author = author

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.blurple)
    async def init_game_callback(
        self, button: Button, interaction: Interaction
    ) -> None:
        await interaction.response.defer()
        if interaction.user.id != self.author:
            await interaction.followup.send(
                embed=MainEmbed("This interaction is not for you"),
                ephemeral=True,
            )
            return

        countdown = datetime.datetime.now() + datetime.timedelta(
            seconds=ROULETTE_AUTOSTART
        )
        countdown = f"<t:{round(countdown.timestamp())}:R>"

        Cache.roulette_active[interaction.guild.id] = {
            "players": PlayerIterator([interaction.user]),
            "chamber": ChamberIterator(random.randint(1, 6)),
            "countdown": countdown,
            "start": False,
            "message": interaction.message,
        }

        await interaction.followup.edit_message(
            interaction.message.id,
            embed=roulette_embedder(interaction.guild.id, interaction.user),
            view=RouletteJoinView(
                interaction.guild.id, interaction.user, interaction.message
            ),
        )

    @discord.ui.button(label="Cancel Game", style=discord.ButtonStyle.red)
    async def cancel_game_callback(
        self, button: Button, interaction: Interaction
    ) -> None:
        await interaction.response.defer()
        if interaction.user.id != self.author:
            await interaction.followup.send(
                embed=MainEmbed("This interaction is not for you"),
                ephemeral=True,
            )
            return

        self.disable_all_items()
        await interaction.followup.edit_message(
            interaction.message.id,
            embed=MainEmbed("The game has been cancelled"),
            view=self,
        )
