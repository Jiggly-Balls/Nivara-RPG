import logging
import time
from typing import final

import asyncpg
from disckit.utils import MainEmbed
from discord import Interaction, app_commands

from backend.cache import Cache
from backend.db_users import UserDB
from backend.errors import DBConnectionException
from core import BaseCog, Bot

logger = logging.getLogger(__name__)


@final
class Misc(BaseCog):
    def __init__(self, bot: Bot) -> None:
        super().__init__(logger=logger)
        self.bot = bot

    misc = app_commands.Group(
        name="misc", description="Miscellaneous commands about the bot."
    )

    @misc.command()
    async def status(self, interaction: Interaction) -> None:
        await interaction.response.defer()

        db_time = time.perf_counter()
        try:
            await UserDB(interaction.user.id).get_account(False)
            db_latency = (
                f"`{round((time.perf_counter() - db_time) * 1000):,} ms`"
            )
        except (DBConnectionException, asyncpg.InternalServerError):
            db_latency = "`DB not connected`"

        total_guilds = len(self.bot.guilds)
        total_users = len(self.bot.users)

        bot_latency = f"`{round(self.bot.latency * 1000):,} ms`"
        status_embed = MainEmbed(title="Nivara's Status")

        if self.bot.user:
            thumbnail = self.bot.user.display_avatar.url
            status_embed.set_thumbnail(url=thumbnail)

        status_embed = (
            status_embed.add_field(
                name="Version", value=f"`{self.bot.version}`", inline=False
            )
            .add_field(name="Bot Latency", value=bot_latency, inline=False)
            .add_field(
                name="Database Latency",
                value=db_latency,
                inline=False,
            )
            .add_field(name="Online Since", value=Cache.uptime, inline=False)
            .add_field(
                name="Last Reconnect", value=Cache.last_reconnect, inline=False
            )
            .add_field(
                name="Present In",
                value=f"`{total_guilds}` guilds",
                inline=False,
            )
            .add_field(
                name="Watching Over",
                value=f"`{total_users}` users",
                inline=False,
            )
        )

        await interaction.followup.send(embed=status_embed)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Misc(bot))
