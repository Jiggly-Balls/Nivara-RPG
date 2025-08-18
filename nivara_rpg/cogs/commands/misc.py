import logging
import time
from typing import final

import asyncpg
import discord
from backend.cache import Cache
from backend.db_users import UserDB
from backend.errors import DBConnectionException
from core import BaseCog, Bot
from core.utils import MainEmbed
from discord import ApplicationContext

logger = logging.getLogger(__name__)


@final
class Misc(BaseCog):
    def __init__(self, bot: Bot) -> None:
        super().__init__(logger=logger)
        self.bot = bot

    misc = discord.SlashCommandGroup(
        "misc", "Miscellaneous commands about the bot."
    )

    @misc.command()
    async def status(self, ctx: ApplicationContext) -> None:
        await ctx.defer()

        db_time = time.perf_counter()
        try:
            await UserDB(ctx.author.id).get_account(False)
            db_latency = (
                f"`{round((time.perf_counter() - db_time) * 1000):,} ms`"
            )
        except (DBConnectionException, asyncpg.InternalServerError):
            db_latency = "`DB not connected`"

        bot_latency = f"`{round(self.bot.latency * 1000):,} ms`"

        thumbnail = None
        if self.bot.user:
            thumbnail = self.bot.user.display_avatar.url

        status_embed = (
            MainEmbed(
                "Nivara's Status",
                thumbnail=thumbnail,
            )
            .add_field(
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
                value=f"`{Cache.guilds}` guilds",
                inline=False,
            )
            .add_field(
                name="Watching Over",
                value=f"`{Cache.users}` users",
                inline=False,
            )
        )

        await ctx.respond(embed=status_embed)


def setup(bot: Bot) -> None:
    bot.add_cog(Misc(bot))
