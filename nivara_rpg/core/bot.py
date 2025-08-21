from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING

from discord.ext import commands

from backend.cache import Cache
from core.meta import get_version

if TYPE_CHECKING:
    from discord import Intents


logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, *, intents: Intents) -> None:
        super().__init__(command_prefix=[], intents=intents)
        self.version: str = get_version() or "Unkown"
        self._connected: bool = False

    async def on_ready(self) -> None:
        Cache.last_reconnect = (
            f"<t:{round(datetime.datetime.now().timestamp())}:R>"
        )

        if not self._connected:
            self._connected = True
            logging.info(f"Logged in as :: {self.user}")
            logging.info("Your life is meaningless.")
        else:
            logging.info("Reconnect.")
