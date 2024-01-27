
from __future__ import annotations

from attrs import define, field

from collections import defaultdict
from typing import Iterable, NamedTuple


@define(eq=False)
class Board:
    # Maps space name position
    spaces_map: dict[str, tuple[int, int]]
    # Maps space name to players
    _position_map: dict[str, list[str]] = field(init=False, factory=lambda: defaultdict(list))
    # Maps player to space
    _player_map: dict[str, str] = field(init=False, factory=dict)

    @property
    def players(self) -> Iterable[str]:
        return self._player_map.keys()

    def add_player(self, player_name: str, starting_space: str) -> None:
        if player_name in self._player_map:
            raise ValueError(f"Player {player_name} already exists")
        if starting_space not in self.spaces_map:
            raise ValueError(f"Space {starting_space} does not exist")
        self._player_map[player_name] = starting_space
        self._position_map[starting_space].append(player_name)

    def remove_player(self, player_name: str) -> None:
        space = self._player_map[player_name]
        del self._player_map[player_name]
        self._position_map[space].remove(player_name)

    def move_player(self, player_name: str, destination_space: str) -> None:
        source_space = self._player_map[player_name]
        self._position_map[source_space].remove(player_name)
        self._player_map[player_name] = destination_space
        self._position_map[destination_space].append(player_name)

    def get_players_at(self, space: str) -> list[str]:
        return self._position_map[space]

    def get_space(self, player_name: str) -> str:
        return self._player_map[player_name]

    def __contains__(self, player_name: str) -> bool:
        return player_name in self._player_map

    def __getitem__(self, player_name: str) -> str:
        """Alias for self.get_space."""
        return self.get_space(player_name)

    def __setitem__(self, player_name: str, destination_space: str) -> None:
        """Calls add_player or move_player as needed."""
        if player_name in self:
            self.move_player(player_name, destination_space)
        else:
            self.add_player(player_name, destination_space)

    def __delitem__(self, player_name: str) -> None:
        """Alias for self.remove_player."""
        self.remove_player(player_name)

    def get_position(self, player_name: str) -> tuple[int, int]:
        space = self.get_space(player_name)
        all_players_at_position = self._position_map[space]
        player_index = all_players_at_position.index(player_name)
        key = DeltaMapKey(player_count=len(all_players_at_position), player_index=player_index)
        base_space_y, base_space_x = self.spaces_map[space]
        delta_y, delta_x = DELTAS[key]
        return base_space_y + delta_y, base_space_x + delta_x


class DeltaMapKey(NamedTuple):
    """The key to the DELTAS map below: A player count together with
    the index of the intended player."""
    player_count: int
    player_index: int


DELTAS = {
    DeltaMapKey(1, 0): (0, 0),
    DeltaMapKey(2, 0): (0, -16),
    DeltaMapKey(2, 1): (0, 16),
    DeltaMapKey(3, 0): (-16, 0),
    DeltaMapKey(3, 1): (0, -16),
    DeltaMapKey(3, 2): (0, 16),
    DeltaMapKey(4, 0): (-16, -16),
    DeltaMapKey(4, 1): (-16, 16),
    DeltaMapKey(4, 2): (16, -16),
    DeltaMapKey(4, 3): (16, 16),
    DeltaMapKey(5, 0): (-16, -16),
    DeltaMapKey(5, 1): (-16, 16),
    DeltaMapKey(5, 2): (0, 0),
    DeltaMapKey(5, 3): (16, -16),
    DeltaMapKey(5, 4): (16, 16),
    DeltaMapKey(6, 0): (-16, -16),
    DeltaMapKey(6, 1): (-16, 16),
    DeltaMapKey(6, 2): (0, -8),
    DeltaMapKey(6, 3): (0, 8),
    DeltaMapKey(6, 4): (16, -16),
    DeltaMapKey(6, 5): (16, 16),
    DeltaMapKey(7, 0): (-16, -16),
    DeltaMapKey(7, 1): (-16, 16),
    DeltaMapKey(7, 2): (-8, 0),
    DeltaMapKey(7, 3): (0, -8),
    DeltaMapKey(7, 4): (0, 8),
    DeltaMapKey(7, 5): (16, -16),
    DeltaMapKey(7, 6): (16, 16),
}
