from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from logging import Logger


class BaseCog(commands.Cog):
    cog_name: str = None

    def __init_subclass__(cls, *, state_name: None | str = None) -> None:
        super().__init_subclass__()
        cls.cog_name = state_name or cls.__name__

    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self.logger = logger

    @discord.Cog.listener()
    async def on_ready(self) -> None:
        self.logger.info(f"{self.cog_name} is ready.")
