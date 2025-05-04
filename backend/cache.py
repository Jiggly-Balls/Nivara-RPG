from __future__ import annotations

from typing import TYPE_CHECKING

from discord import MISSING

if TYPE_CHECKING:
    from data.games.roulette import RouletteData


class Cache:
    uptime: str = MISSING
    last_reconnect: str = MISSING
    users: int = MISSING
    guilds: int = MISSING

    roulette_active: dict[int, RouletteData] = {}
