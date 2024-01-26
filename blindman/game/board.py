
from __future__ import annotations

from blindman.game.object.sprite import Sprite
from blindman.game.object.event_manager import Event, create_object_event

from attrs import define, field

from typing import Protocol


@define
class Board:
    delegate: BoardEventDelegate
    spaces_map: dict[str, tuple[int, int]]  # Maps space name position
    player_map: dict[str, str] = field(factory=dict)  # Maps player name to space name

    def __init__(self, spaces_map: dict[str, tuple[int, int]]):
        self.spaces_map = spaces_map
        self.player_map = {}

    def add_player(self, player: Sprite, starting_space: str) -> None:
        player_name = player.name
        if player_name is None:
            raise ValueError("Player sprite must have a name to be stored in a Board instance")
        if player_name in self.player_map:
            raise ValueError(f"Player {player_name} already exists")
        self.player_map[player_name] = starting_space
        self.delegate.append_event(create_object_event(lambda _: player))


class BoardEventDelegate(Protocol):

    def append_event(self, *events: Event) -> None:
        ...

    def wait(self, delta: int) -> None:
        ...
