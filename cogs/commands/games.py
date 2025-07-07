import logging
from typing import final

import discord
from discord import ApplicationContext

from core import BaseCog, Bot
from core.views.games_view import MineGameView
from data.games.mine import MineEngine

logger = logging.getLogger(__name__)


@final
class Games(BaseCog):
    games_group = discord.SlashCommandGroup(
        "games", "Fun games to play with your friends!"
    )

    roulette_group = games_group.create_subgroup(
        "twisted-roulette", "Play the twisted roulette with your friends!"
    )

    def __init__(self, bot: Bot) -> None:
        super().__init__(logger=logger)
        self.bot = bot

    @games_group.command()
    async def mine(self, ctx: ApplicationContext) -> None:
        await ctx.defer()
        miner = MineEngine()
        miner.create_map()
        image = miner.create_image()
        await ctx.respond(image, view=MineGameView(ctx.author.id, miner))


def setup(bot: Bot) -> None:
    bot.add_cog(Games(bot))
