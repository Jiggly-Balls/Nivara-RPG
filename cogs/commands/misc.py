import logging
import time

import discord
from discord import ApplicationContext

from backend.cache import Cache
from backend.db_users import UserDB
from core.base_cog import BaseCog
from core.bot import Bot
from core.meta import get_version
from core.utils import MainEmbed

logger = logging.getLogger(__name__)


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
        await UserDB(ctx.author.id).get_account(False)

        db_latency = round((time.perf_counter() - db_time) * 1000)
        bot_latency = round(self.bot.latency * 1000)

        status_embed = (
            MainEmbed(
                "Nivara's Status",
                thumbnail=self.bot.user.display_avatar.url,
            )
            .add_field(name="Version", value=get_version(), inline=False)
            .add_field(
                name="Bot Latency", value=f"`{bot_latency} ms`", inline=False
            )
            .add_field(
                name="Database Latency",
                value=f"`{db_latency} ms`",
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
