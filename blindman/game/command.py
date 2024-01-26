
from .board import Board
from .timeline import TimelineLike
from .error import InputParseError
from .movement import MovementPlanner, MovementType

import cattrs

from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Any


class Command(ABC):
    """A command acts on a Board."""

    @abstractmethod
    def execute(self, board: Board, timeline: TimelineLike) -> None:
        ...


@dataclass(frozen=True)
class MovePlayerCommand(Command):
    player_name: str
    destination_space: str

    def execute(self, board: Board, timeline: TimelineLike) -> None:
        planner = MovementPlanner(board)

        source_space = board.get_space(self.player_name)
        for player in board.get_players_at(source_space):
            planner.add_player(player, MovementType.SHORT)
        for player in board.get_players_at(self.destination_space):
            planner.add_player(player, MovementType.SHORT)
        planner.add_player(player, MovementType.LONG)

        board.move_player(self.player_name, self.destination_space)

        planner.take_destination_snapshot()
        planner.produce_movement(timeline)


@dataclass(frozen=True)
class WaitCommand(Command):
    frames: int

    def execute(self, board: Board, timeline: TimelineLike) -> None:
        timeline.wait(self.frames)


COMMAND_REGISTRY: dict[str, type]
COMMAND_REGISTRY = {
    'move': MovePlayerCommand,
    'wait': WaitCommand,
}


def parse_command(command_sexpr: Any) -> Command:
    if not isinstance(command_sexpr, list):
        raise InputParseError(f"Expected list for command, got {command_sexpr}")
    if not command_sexpr:
        raise InputParseError("Expected non-empty list for command")

    command_type = COMMAND_REGISTRY[str(command_sexpr[0])]
    return cattrs.structure_attrs_fromtuple(tuple(command_sexpr[1:]), command_type)
