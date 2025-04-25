from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING

import discord

from backend.cache import Cache

if TYPE_CHECKING:
    from discord import Intents


logger = logging.getLogger(__name__)


class Bot(discord.Bot):
    def __init__(self, *, intents: Intents) -> None:
        super().__init__(intents=intents)

    async def on_ready(self) -> None:
        Cache.last_reconnect = (
            f"<t:{round(datetime.datetime.now().timestamp())}:R>"
        )

        logging.info(f"Logged in as :: {self.user}")
        logging.info("Your life is meaningless.")
