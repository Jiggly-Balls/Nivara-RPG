import logging
import sys
import traceback

import discord
from discord.ext import commands

from core import BaseCog, Bot
from core.utils import ErrorEmbed
from data.constants.core import LOGGING_CHANNEL

logger = logging.getLogger(__name__)


class ErrorHandler(BaseCog):
    def __init__(self, bot: Bot) -> None:
        super().__init__(logger=logger)
        self.bot = bot

    @commands.Cog.listener()  # pyright:ignore[reportUntypedFunctionDecorator]
    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error: discord.DiscordException
    ) -> None:
        if isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.respond(
                embed=ErrorEmbed(
                    f"I'm missing the following permission(s) to execute this command:"
                    f"\n{', '.join(error.missing_permissions)}"
                )
            )

        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.respond(
                embed=ErrorEmbed(
                    f"You're missing the following permission(s) to execute this command:"
                    f"\n{', '.join(error.missing_permissions)}"
                )
            )

        else:
            await ctx.respond(
                embed=ErrorEmbed(
                    "Sorry :(",
                    "An unexpected error has occurred. The developers have been notified of this.",
                )
            )

            print(
                f"Ignoring exception in command {ctx.command}:",
                file=sys.stderr,
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )

            channel = self.bot.get_channel(
                LOGGING_CHANNEL
            ) or await self.bot.fetch_channel(LOGGING_CHANNEL)

            frame = (
                error.__traceback__.tb_frame
                if error.__traceback__
                else "Unkown"
            )

            description = (
                f"```\nError caused by-\nAuthor Name: {ctx.author}"
                f"\nAuthor ID: {ctx.author.id}\n"
                f"\nError Type-\n{type(error)}\n"
                f"\nError Type Description-\n{frame}\n"
                f"\nCause-\n{error.with_traceback(error.__traceback__)}```"
            )

            await channel.send(  # pyright:ignore[reportAttributeAccessIssue]
                embed=ErrorEmbed(
                    f"Error in command: {ctx.command}",
                    description,
                )
            )


def setup(bot: Bot) -> None:
    bot.add_cog(ErrorHandler(bot))
