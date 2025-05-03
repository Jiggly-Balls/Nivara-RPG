from __future__ import annotations

from typing import TYPE_CHECKING

from discord import MISSING

if TYPE_CHECKING:
    from discord import Message

    from data.games.roulette import ChamberIterator, PlayerIterator


class Cache:
    uptime: str = MISSING
    last_reconnect: str = MISSING
    users: int = MISSING
    guilds: int = MISSING

    roulette_active: dict[
        int, dict[str, PlayerIterator | ChamberIterator | str | bool | Message]
    ] = {}
