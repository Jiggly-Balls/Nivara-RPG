from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

    from discord import Member, Message, User


@dataclass
class RouletteData:
    players: PlayerIterator
    chamber: ChamberIterator
    countdown: str
    start: bool
    message: Message


class PlayerIterator:
    def __init__(self, player_list: list[Member | User]) -> None:
        self.player_list = player_list
        self.current_player: Member = self.player_list[0]
        self.dead_players: list[Member | User] = []
        self.current_player_index: int = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> None:
        self.current_player_index += 1
        self._check_player()
        self.current_player = self.player_list[self.current_player_index]

    def _check_player(self) -> None:
        if self.current_player_index > len(self.player_list) - 1:
            self.current_player_index = 0

    def kill(self, player: Member | User) -> None:
        self.player_list.remove(player)
        self.dead_players.append(player)
        self._check_player()


class ChamberIterator:
    def __init__(self, loaded_chamber: int) -> None:
        self.loaded_chamber = loaded_chamber
        self.current_chamber = 1

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> None:
        self.current_chamber += 1
        if self.current_chamber > 6:
            self.current_chamber = 1

    def check_hit(self) -> bool:
        return self.current_chamber == self.loaded_chamber
