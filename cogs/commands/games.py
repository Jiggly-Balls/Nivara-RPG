import logging
from pprint import pprint

import discord
from discord import ApplicationContext
from discord.commands import option

from backend.db_users import UserAspect, UserDB
from core.base_cog import BaseCog
from core.bot import Bot

logger = logging.getLogger(__name__)


class Games(BaseCog):
    def __init__(self, bot: Bot) -> None:
        super().__init__(logger=logger)
        self.bot = bot

    games = discord.SlashCommandGroup(
        "games", "Fun games to play with your friends!"
    )

    @games.command()
    async def test(self, ctx: ApplicationContext) -> None:
        player = UserDB(ctx.author.id)
        await player.post_account()

        await ctx.respond(embed=discord.Embed(description="Created account"))

    @games.command()
    @option("id", required=False)
    async def test2(self, ctx: ApplicationContext, id: str) -> None:
        await ctx.defer()

        id: int = int(id) if id else ctx.author.id
        player = UserDB(id)
        player_data = await player.get_account()

        print(type(player_data))
        print()
        print()
        pprint(dir(player_data))
        print()
        print()
        pprint(player_data)

        await ctx.followup.send(content="DONE")

    @games.command()
    async def test3(self, ctx: ApplicationContext, value: int) -> None:
        await ctx.defer()

        player = UserDB(ctx.author.id)
        await player.update_aspect(UserAspect.exp, value=value)

        await ctx.followup.send(content=f"Updated EXP to: {value}")


def setup(bot: Bot) -> None:
    bot.add_cog(Games(bot))
