from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands
from discord.utils import MISSING

if TYPE_CHECKING:
    from logging import Logger


class BaseCog(commands.Cog):
    cog_name: str = MISSING

    def __init_subclass__(cls, *, cog_name: None | str = None) -> None:
        super().__init_subclass__()
        cls.cog_name = cog_name or cls.__name__

    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self.logger: Logger = logger

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.logger.info(f"{self.cog_name} is ready.")
