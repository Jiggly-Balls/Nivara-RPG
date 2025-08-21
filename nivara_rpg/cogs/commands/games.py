import logging
from typing import final

from discord import Interaction, app_commands

from core import BaseCog, Bot
from core.views.games_view import MineGameView
from data.games.mine import MineEngine

logger = logging.getLogger(__name__)


@final
class Games(BaseCog):
    games_group = app_commands.Group(
        name="games", description="Fun games to play with your friends!"
    )

    # roulette_group = app_commands.Group(
    #     parent=games_group,
    #     name="twisted-roulette",
    #     description="Play the twisted roulette with your friends!",
    # )

    def __init__(self, bot: Bot) -> None:
        super().__init__(logger=logger)
        self.bot = bot

    @games_group.command()
    async def mine(self, interaction: Interaction) -> None:
        await interaction.response.defer()

        miner = MineEngine()
        miner.create_map()
        image = miner.create_image()

        await interaction.followup.send(
            image, view=MineGameView(interaction.user.id, miner)
        )


async def setup(bot: Bot) -> None:
    await bot.add_cog(Games(bot))
