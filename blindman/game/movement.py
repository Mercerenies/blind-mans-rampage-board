
"""Movement-planning utility for generating move events."""

from __future__ import annotations

from blindman.game.object.events import MoveObjectController

from attrs import define, field, evolve

from enum import IntEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board, BoardEventDelegate


class MovementType(IntEnum):
    """Whether the movement is a simple adjustment of position (SHORT)
    or a significant movement to another part of the board (LONG).
    MovementTypes are ordered, and more significant movements are
    considered greater.

    """
    SHORT = auto()
    LONG = auto()


MOVEMENT_LENGTHS = {
    MovementType.SHORT: 30,
    MovementType.LONG: 60,
}


@define
class MovementPlanner:
    """Class to generate move events.

    MovementPlanner monitors the board for changes in player positions
    in preparation to create one or more MoveObjectController.event
    events. This class should be constructed (and players added to it)
    before any players are moved on the board. After movement has
    occurred, call take_destination_snapshot to scan the board for
    changes and prepare the animations.

    """
    _board: Board
    _players: dict[str, PlayerMovement] = field(init=False, factory=dict)

    def add_player(self, player_name: str, movement_type: MovementType) -> None:
        """Adds the player to the current movement. If the player is
        already involved in the current movement, the existing entry
        is updated with a new source and the maximum of the two
        movement types.

        """
        pos = self._board.get_position(player_name)
        if player_name in self._players:
            self._players[player_name] = evolve(
                self._players[player_name],
                source=pos,
                destination=pos,
                movement_type=max(movement_type, self._players[player_name].movement_type),
            )
        else:
            self._players[player_name] = PlayerMovement(
                player_name=player_name,
                movement_type=movement_type,
                source=pos,
                destination=pos,
            )

    def take_destination_snapshot(self) -> None:
        """Update all player objects in the current movement to mark
        their current position on the board as their destination."""
        for player_name in self._players:
            destination = self._board.get_position(player_name)
            self._players[player_name] = evolve(self._players[player_name], destination=destination)

    def produce_movement(self, delegate: BoardEventDelegate | None = None) -> None:
        if delegate is None:
            delegate = self._board.delegate
        for player in self._players.values():
            total_frames = MOVEMENT_LENGTHS[player.movement_type]
            delegate.append_event(
                MoveObjectController.event(
                    object_name=player.player_name,
                    new_pos=player.destination,
                    total_frames=total_frames,
                ),
            )

        max_length = max(MOVEMENT_LENGTHS[m.movement_type] for m in self._players.values())
        delegate.wait(max_length)


@define(frozen=True)
class PlayerMovement:
    player_name: str = field()
    movement_type: MovementType = field()
    source: tuple[int, int] = field()
    destination: tuple[int, int] = field()

    @destination.default
    def _default_destination(self) -> tuple[int, int]:
        return self.source
