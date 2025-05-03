import logging

import discord
from discord import ApplicationContext

from backend.cache import Cache
from core import BaseCog, Bot
from core.utils import MainEmbed
from core.views.games_view import (
    MineGameView,
    RouletteInitView,
    roulette_embedder,
)
from data.games.mine import MineEngine

logger = logging.getLogger(__name__)


class Games(BaseCog):
    games_group = discord.SlashCommandGroup(
        "games", "Fun games to play with your friends!"
    )

    roulette_group = games_group.create_subgroup(
        "twisted-roulette", "Play the twisted roulette with your friends!"
    )

    def __init__(self, bot: Bot) -> None:
        super().__init__(logger=logger)
        self.bot = bot

    @games_group.command()
    async def mine(self, ctx: ApplicationContext) -> None:
        await ctx.defer()
        miner = MineEngine()
        miner.create_map()
        image = miner.create_image()
        await ctx.respond(image, view=MineGameView(ctx.author.id, miner))

    @roulette_group.command()
    async def start(self, ctx: ApplicationContext) -> None:
        await ctx.defer()

        if ctx.guild.id in Cache.roulette_active:
            return await ctx.respond(
                embed=MainEmbed(
                    "There is already an on going game in this server. Wait till it gets over to start a new one."
                )
            )

        await ctx.respond(
            embed=MainEmbed("Welcome to Twisted Russian Roulette!"),
            view=RouletteInitView(ctx.author.id),
        )

    @roulette_group.command()
    async def join(self, ctx: ApplicationContext) -> None:
        await ctx.defer()

        if ctx.guild.id not in Cache.roulette_active:
            return await ctx.followup.send(
                embed=MainEmbed(
                    "There is no active game in the current server."
                ),
                ephemeral=True,
            )

        elif (
            ctx.author
            in Cache.roulette_active[ctx.guild.id]["players"].player_list
        ):
            return await ctx.followup.send(
                embed=MainEmbed("You're already a part of the game."),
                ephemeral=True,
            )

        elif Cache.roulette_active[ctx.guild.id]["start"]:
            return await ctx.followup.send(
                embed=MainEmbed(
                    "You cannot join an on-going game. Wait till it gets over."
                ),
                ephemeral=True,
            )

        Cache.roulette_active[ctx.guild.id]["players"].player_list.append(
            ctx.author
        )
        await ctx.followup.send(
            embed=MainEmbed("You have successfully joined!"), ephemeral=True
        )

        await Cache.roulette_active[ctx.guild.id]["message"].edit(
            embed=roulette_embedder(ctx.guild.id, ctx.author)
        )

    @roulette_group.command()
    async def leave(self, ctx: ApplicationContext) -> None:
        await ctx.defer()

        if ctx.guild.id not in Cache.roulette_active:
            return await ctx.send_followup(
                embed=MainEmbed(
                    "There is no active game in the current server."
                ),
                ephemeral=True,
            )

        elif (
            ctx.author
            not in Cache.roulette_active[ctx.guild.id]["players"].player_list
        ):
            return await ctx.send_followup(
                embed=MainEmbed("You're not a part of the game yet."),
                ephemeral=True,
            )

        elif Cache.roulette_active[ctx.guild.id]["start"]:
            return await ctx.send_followup(
                embed=MainEmbed("You cannot leave an on-going game."),
                ephemeral=True,
            )

        Cache.roulette_active[ctx.guild.id]["players"].player_list.remove(
            ctx.author
        )
        await ctx.send_followup(
            embed=MainEmbed("You have left the game."), ephemeral=True
        )

        await Cache.roulette_active[ctx.guild.id]["message"].edit(
            embed=roulette_embedder(ctx.guild.id, ctx.author)
        )


def setup(bot: Bot) -> None:
    bot.add_cog(Games(bot))
