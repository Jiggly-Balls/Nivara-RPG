"""
Nivara RPG
~~~~~~~~~~

A fun RPG bot for your discord server.

:copyright: (c) 2025-present Jiggly Balls
:license: MIT License, see LICENSE for more details.
"""

__title__ = "Nivara RPG"
__author__ = "Jiggly Balls"
__license__ = "MIT License"
__copyright__ = "Copyright 2025-present Jiggly Balls"


import asyncio
import datetime
import logging
import os

import discord
import dotenv
from discord import MISSING
from sqlalchemy.ext.asyncio import create_async_engine

from backend.base_db import BaseData
from backend.cache import Cache
from backend.tables import BaseTable
from core import Bot, setup_logging
from data.constants.core import EXTENSION_DIRECTORY

ENV = dotenv.dotenv_values(".env")
TOKEN = ENV["TOKEN"]
CONNECTION_STRING = ENV["CONNECTION_STRING"]
intents = discord.Intents.none()


logging.basicConfig(
    filename="bot.log",
    filemode="w",
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
)

logging.getLogger("discord").setLevel(logging.ERROR)
setup_logging()

logger = logging.getLogger()


def load_extensions(bot: Bot) -> None:
    for folder in os.listdir(EXTENSION_DIRECTORY):
        for cog in os.listdir(EXTENSION_DIRECTORY + "/" + folder):
            if cog.endswith(".py"):
                cog_path = EXTENSION_DIRECTORY + "." + folder + "." + cog[:-3]
                bot.load_extension(cog_path)
                logging.info(f"Loading Extension: {cog_path}")


async def main() -> None:
    try:
        if CONNECTION_STRING is None:
            raise RuntimeError(
                "No 'CONNECTION_STRING' was provided in the .env file"
            )

        if TOKEN is None:
            raise RuntimeError("No 'TOKEN' was provided in the .env file")

        bot = Bot(intents=intents)
        BaseData.db_engine = create_async_engine(CONNECTION_STRING)
        Cache.uptime = f"<t:{round(datetime.datetime.now().timestamp())}:R>"

        async with BaseData.db_engine.begin() as conn:
            await conn.run_sync(BaseTable.metadata.create_all)

        load_extensions(bot=bot)

        await bot.start(TOKEN)

    finally:
        if BaseData.db_engine is not MISSING:
            await BaseData.db_engine.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Exited due to keyboard interrupt.")
