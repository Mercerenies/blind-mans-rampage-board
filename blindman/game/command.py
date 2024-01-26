
from .board import Board
from .error import InputParseError

import cattrs

from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Any


class Command(ABC):
    """A command acts on a Board."""

    @abstractmethod
    def execute(self, board: Board) -> None:
        ...


@dataclass(frozen=True)
class MovePlayerCommand(Command):
    player_name: str
    destination_space: str

    def execute(self, board: Board) -> None:
        board.move_player(self.player_name, self.destination_space)


@dataclass(frozen=True)
class WaitCommand(Command):
    frames: int

    def execute(self, board: Board) -> None:
        board.delegate.wait(self.frames)


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
