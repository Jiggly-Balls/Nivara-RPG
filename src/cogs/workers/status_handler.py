from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, final

import discord
from discord.ext import tasks

from backend.cache import Cache
from core.base_cog import BaseCog
from data.constants.core import STATUS_INTERVAL

if TYPE_CHECKING:
    from collections.abc import Iterator

    from core.bot import Bot


logger = logging.getLogger(__name__)


@final
class StatusHandler(BaseCog):
    def __init__(self, bot: Bot) -> None:
        super().__init__(logger=logger)
        self.bot = bot
        self.notify: bool = False
        self.status: None | Iterator[str] = None

    @discord.Cog.listener()
    async def on_ready(self) -> None:
        await super().on_ready()
        self.status_task.start()

    @tasks.loop(seconds=STATUS_INTERVAL)
    async def status_task(self) -> None:
        await self.bot.wait_until_ready()

        if not self.notify:
            logger.info("Status handler has started.")
            self.notify = True

        await asyncio.sleep(1)

        if self.status is None:
            self.status = await self._calculate_stats()

        try:
            current_status = next(self.status)
        except StopIteration:
            self.status = await self._calculate_stats()
            current_status = next(self.status)

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=current_status
            )
        )

    async def _calculate_stats(self) -> Iterator[str]:
        Cache.users = len(self.bot.users)
        Cache.guilds = len(self.bot.guilds)

        return iter(
            # Prefixed by "Listening to"
            (
                f"version {self.bot.version}",
                f"humans in {Cache.guilds:,} Servers!",
                f"{Cache.users:,} users!",
                "Slash Commands!",
            )
        )


def setup(bot: Bot) -> None:
    bot.add_cog(StatusHandler(bot))
