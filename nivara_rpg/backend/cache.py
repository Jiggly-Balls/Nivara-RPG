from __future__ import annotations

from discord.utils import MISSING


class Cache:
    uptime: str = MISSING
    last_reconnect: str = MISSING
    users: int = MISSING
    guilds: int = MISSING
