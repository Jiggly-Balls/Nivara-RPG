import asyncio
import datetime
import logging
import os

import discord
import dotenv

from backend.cache import Cache
from core import Bot, setup_logging
from data.constants.core_constants import EXTENSION_DIRECTORY

ENV = dotenv.dotenv_values(".env")
TOKEN = ENV["TOKEN"]
intents = discord.Intents.none()


logging.basicConfig(
    filename="bot.log",
    filemode="w",
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(lineno)d] %(message)s",
)
logging.getLogger("discord").setLevel(logging.ERROR)
setup_logging()


def load_extensions(bot: Bot) -> None:
    for folder in os.listdir(EXTENSION_DIRECTORY):
        for cog in os.listdir(EXTENSION_DIRECTORY + "/" + folder):
            if cog.endswith(".py"):
                cog_path = EXTENSION_DIRECTORY + "." + folder + "." + cog[:-3]
                bot.load_extension(cog_path)
                logging.info(f"Loading Extension: {cog_path}")


async def main() -> None:
    bot = Bot(intents=intents)
    load_extensions(bot=bot)
    Cache.uptime = f"<t:{round(datetime.datetime.now().timestamp())}:R>"

    if TOKEN is None:
        raise RuntimeError("No token was provided in the .env file.")

    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
