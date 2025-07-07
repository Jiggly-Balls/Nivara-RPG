from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from core.utils import ErrorEmbed
from core.views.base_view import BaseView
from data.games.mine import Direction, MineEngine

if TYPE_CHECKING:
    from discord import Interaction


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


class MineGameView(BaseView):
    def __init__(self, author: int, engine: MineEngine) -> None:
        super().__init__(timeout=300, disable_on_timeout=True)

        self.author = author
        self.engine = engine

        self.add_item(MineButton(emoji="⬆", direction=Direction.UP))
        self.add_item(MineButton(emoji="⬇", direction=Direction.DOWN))
        self.add_item(MineButton(emoji="⬅", direction=Direction.LEFT))
        self.add_item(MineButton(emoji="➡", direction=Direction.RIGHT))
