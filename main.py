import asyncio
import datetime
import logging
import os

import discord
import dotenv

from backend.base_db import BaseData
from backend.base_pg import create_base_pool_connection
from backend.cache import Cache
from core import Bot, setup_logging
from data.constants.core import EXTENSION_DIRECTORY

ENV = dotenv.dotenv_values(".env")
TOKEN = ENV["TOKEN"]
DB_HOST = ENV["DB_HOST"]
DB_PASSWORD = ENV["DB_PASSWORD"]
DB_NAME = ENV["DB_NAME"]
DB_PORT = ENV["DB_PORT"]
DB_USER = ENV["DB_USER"]
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
    async with create_base_pool_connection(
        host=DB_HOST,
        database=DB_NAME,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        max_inactive_connection_lifetime=0,
    ) as pool:
        logger.info("Connected to database")

        bot = Bot(intents=intents)
        BaseData.db_connection = pool
        Cache.uptime = f"<t:{round(datetime.datetime.now().timestamp())}:R>"

        load_extensions(bot=bot)

        if TOKEN is None:
            raise RuntimeError("No token was provided in the .env file.")

        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
