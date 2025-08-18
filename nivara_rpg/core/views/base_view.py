from __future__ import annotations

import sys
import traceback
from typing import TYPE_CHECKING

import discord
from core.utils import ErrorEmbed, type_guarantee
from data.constants.core import LOGGING_CHANNEL
from discord.ext import commands

if TYPE_CHECKING:
    from typing import Any

    from discord import Interaction
    from discord.ui import Item


class BaseView(discord.ui.View):
    def __inti__(
        self,
        *items: Item[Any],
        timeout: float | None = 180.0,
        disable_on_timeout: bool = False,
    ) -> None:
        super().__init__(
            *items, timeout=timeout, disable_on_timeout=disable_on_timeout
        )

    async def on_error(
        self, error: Exception, item: Item[Any], interaction: Interaction
    ) -> None:
        if TYPE_CHECKING and not type_guarantee(
            interaction.user, discord.Member, discord.User
        ):
            return

        if isinstance(error, commands.errors.BotMissingPermissions):
            await interaction.respond(
                embed=ErrorEmbed(
                    f"I'm missing the following permission(s) to execute this command:"
                    f"\n{', '.join(error.missing_permissions)}"
                )
            )

        elif isinstance(error, commands.errors.MissingPermissions):
            await interaction.respond(
                embed=ErrorEmbed(
                    f"You're missing the following permission(s) to execute this command:"
                    f"\n{', '.join(error.missing_permissions)}"
                )
            )

        else:
            await interaction.respond(
                embed=ErrorEmbed(
                    "Sorry :(",
                    "An unexpected error has occurred. The developers have been notified of this.",
                )
            )

            print(
                f"Ignoring exception in view {item.view or self} for item {item}:",
                file=sys.stderr,
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )

            channel = interaction.client.get_channel(
                LOGGING_CHANNEL
            ) or await interaction.client.fetch_channel(LOGGING_CHANNEL)

            frame = (
                error.__traceback__.tb_frame
                if error.__traceback__
                else "Unkown"
            )

            description = (
                "```"
                f"\nError in view-\n{item.view or self}\n"
                f"\nError in item-\n{item}\n"
                f"\nError caused by-\nAuthor Name: {interaction.user}"
                f"\nAuthor ID: {interaction.user.id}\n"
                f"\nError Type-\n{type(error)}\n"
                f"\nError Type Description-\n{frame}\n"
                f"\nCause-\n{error.with_traceback(error.__traceback__)}"
                "```"
            )

            await channel.send(  # pyright:ignore[reportAttributeAccessIssue]
                embed=ErrorEmbed(
                    "Error caused in a view",
                    description,
                )
            )
