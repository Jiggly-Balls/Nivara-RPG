from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import discord

from core.base_cog import BaseCog

if TYPE_CHECKING:
    from discord import ApplicationContext

    from core.bot import Bot


logger = logging.getLogger(__name__)


class Games(BaseCog):
    def __init__(self, bot: Bot) -> None:
        super().__init__(logger=logger)
        self.bot = bot

    games = discord.SlashCommandGroup(
        "games", "Fun games to play with your friends!"
    )

    @games.command()
    async def test(self, ctx: ApplicationContext) -> None:
        await ctx.respond(embed=discord.Embed(description="Testing"))


def setup(bot: Bot) -> None:
    bot.add_cog(Games(bot))
