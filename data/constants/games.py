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
