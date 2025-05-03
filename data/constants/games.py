from enum import Enum, IntEnum, StrEnum, auto
from functools import cache


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class MineAssets(StrEnum):
    PLAYER = "<:player:1367933647071481927>"
    EMPTY = "<:empty:1367923622567481492>"
    STONE = "<:stone:1367923699755257866>"
    COBBLESTONE = "<:cobblestone:1367923579018154044>"
    COAL = "<:coal:1367923490069549066>"
    IRON = "<:iron:1367923677403807906>"
    GOLD = "<:gold:1367923658538090576>"
    DIAMOND = "<:diamond:1367923600958423052>"


class MineRates(IntEnum):
    STONE = 30
    COBBLESTONE = 27
    COAL = 20
    IRON = 15
    GOLD = 7
    DIAMOND = 1


@cache
def asset_rate_bind() -> tuple[list[MineAssets], list[int]]:
    names: list[MineAssets] = []
    rates: list[int] = []
    asset_map: dict[str, MineAssets] = MineAssets._member_map_

    for name, rate in MineRates._member_map_.items():
        names.append(asset_map[name])
        rates.append(rate.value)

    return names, rates


# 0 -> Killer
# 1 -> Victim
ROULETTE_KILL_TEXTS: tuple[str, ...] = (
    "{0} blew {1}'s head off!",
    "And that's a headshot! {1} was killed by {0}.",
    "{1} was destroyed by {0}!",
    "{1} killed by {0}. Now that's one step closer to winning!",
)

ROULETTE_MISS_TEXTS: tuple[str, ...] = (
    "{0} tried killing {1} but seems like their luck ran out.",
    "{0} tried killing {1} but they missed their shot!",
    "{0} pulled the trigger at {1} but the chamber was empty!",
)

ROULETTE_SUICIDE_KILL_TEXTS: tuple[str, ...] = (
    "{} decided to gamble it all and died to themself!",
    "Seems like {}'s luck ran out and died to themself!"
)

ROULETTE_SUICIDE_MISS_TEXTS: tuple[str, ...] = (
    "{} decided to gamble it all and survived! They get an extra round to shoot!",
    "{} tried to shoot themself and survived! They get an extra round to shoot!",
)
