import datetime

import discord

from backend.cache import Cache


class Bot(discord.Bot):
    def __init__(self) -> None:
        super().__init__()

    async def on_ready(self) -> None:
        Cache.last_reconnect = (
            f"<t:{round(datetime.datetime.now().timestamp())}:R>"
        )

        print("\n============================\n")
        print(f"Logged in as :: {self.user}")
        print("Your life is meaningless.")
        print("\n============================\n")
