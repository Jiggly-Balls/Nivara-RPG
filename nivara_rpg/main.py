"""
Nivara RPG
~~~~~~~~~~

A fun RPG bot for your discord server.

:copyright: (c) 2025-present Jiggly Balls
:license: MIT License, see LICENSE for more details.
"""

__title__ = "Nivara RPG"
__author__ = "Jiggly Balls"
__license__ = "GPL-2.0 License"
__copyright__ = "Copyright 2025-present Jiggly Balls"


import asyncio
import datetime
import logging
import os

import asyncpg
import discord
import dotenv
from backend.base_db import BaseData
from backend.cache import Cache
from backend.tables import BaseTable
from core import Bot, setup_logging
from data.constants.core import EXTENSION_DIRECTORY
from discord import MISSING
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

ENV = dotenv.dotenv_values(".env")
TOKEN = ENV["TOKEN"]
CONNECTION_STRING = ENV["CONNECTION_STRING"]
intents = discord.Intents(guilds=True, members=True)


discord.VoiceClient.warn_nacl = False
logging.basicConfig(
    filename="bot.log",
    filemode="w",
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
)

logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
setup_logging()

logger = logging.getLogger()


def load_extensions(*, bot: Bot, directory: str) -> None:
    """Loads all the extensions from the supplied directory.

    Parameters
    ----------
    directory
        The directory containing the cogs.
    """
    parent = directory.split("/")[1]

    for folder in os.listdir(directory):
        for cog in os.listdir(directory + "/" + folder):
            if cog.endswith(".py"):
                cog_path = (
                    parent.replace("/", ".") + "." + folder + "." + cog[:-3]
                )
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
        try:
            BaseData.db_engine = create_async_engine(
                CONNECTION_STRING, pool_pre_ping=True
            )
            BaseData.session_factory = async_sessionmaker(
                BaseData.db_engine, expire_on_commit=True
            )
            async with BaseData.db_engine.begin() as conn:
                await conn.run_sync(BaseTable.metadata.create_all)
        except asyncpg.InternalServerError as error:
            logger.warning("Couldn't connect to database : %s", str(error))

        load_extensions(bot=bot, directory=EXTENSION_DIRECTORY)
        Cache.uptime = f"<t:{round(datetime.datetime.now().timestamp())}:R>"
        await bot.start(TOKEN)

    finally:
        if BaseData.db_engine is not MISSING:
            logger.info("Attempting to close database connection.")
            await BaseData.db_engine.dispose()
            logger.info("Closed database connection.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Exited due to keyboard interrupt.")
