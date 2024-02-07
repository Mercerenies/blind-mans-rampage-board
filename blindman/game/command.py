
"""Commands that affect the board and timeline."""

from .board import Board
from .timeline import TimelineLike
from .error import InputParseError
from .movement import MovementPlanner, MovementType, MOVEMENT_LENGTHS
from .image import resolve_image_path
from blindman.game.object.sprite import Sprite
from blindman.game.object.text import Text, TEXT_OBJECT_NAME
from blindman.game.object.events import FadeObjectController
from blindman.game.object.background import FadeBackgroundController

import cattrs

from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from blindman.game.engine import GameEngine


class Command(ABC):
    """A command acts on a Board."""

    @abstractmethod
    def execute(self, board: Board, timeline: TimelineLike) -> None:
        ...


@dataclass(frozen=True)
class MovePlayerCommand(Command):
    """Command to move the player to a new space."""

    player_name: str
    destination_space: str

    def execute(self, board: Board, timeline: TimelineLike) -> None:
        with MovementPlanner(board, timeline) as planner:
            planner.add_player(self.player_name, MovementType.LONG)
            board[self.player_name] = self.destination_space


@dataclass(frozen=True)
class SwapPlayerCommand(Command):
    """Command to swap the positions of two players.

    Precondition: first_player != second_player

    """

    first_player: str
    second_player: str

    def execute(self, board: Board, timeline: TimelineLike) -> None:
        with MovementPlanner(board, timeline) as planner:
            planner.add_player(self.first_player, MovementType.LONG)
            planner.add_player(self.second_player, MovementType.LONG)
            board[self.first_player], board[self.second_player] = board[self.second_player], board[self.first_player]


@dataclass(frozen=True)
class AddPlayerCommand(Command):
    """Command to add a new player to the board, with a fade-in
    animation."""

    player_name: str
    image_path: str
    space: str

    def execute(self, board: Board, timeline: TimelineLike) -> None:
        animation_time = MOVEMENT_LENGTHS[MovementType.SHORT]
        with MovementPlanner(board, timeline):  # Movement planner for same-space adjustments
            position = board.spaces_map[self.space]
            image = resolve_image_path(self.image_path)
            board[self.player_name] = self.space

            def _factory(_):
                return Sprite(position, image, self.player_name, alpha=0.0)
            timeline.append_event(FadeObjectController.fade_in_event(_factory, animation_time))


@dataclass(frozen=True)
class DestroyPlayerCommand(Command):
    """Command to remove a player from the board, with a fade-out
    animation."""

    player_name: str

    def execute(self, board: Board, timeline: TimelineLike) -> None:
        animation_time = MOVEMENT_LENGTHS[MovementType.SHORT]
        with MovementPlanner(board, timeline):  # Movement planner for same-space adjustments
            del board[self.player_name]
            timeline.append_event(FadeObjectController.fade_out_event(self.player_name, animation_time))


@dataclass(frozen=True)
class SetTextCommand(Command):
    """Command to set the status text for the image, which is
    displayed at the bottom-center of the canvas."""
    text: str

    def execute(self, board: Board, timeline: TimelineLike) -> None:
        def _event(engine: 'GameEngine') -> None:
            if engine.has_object(TEXT_OBJECT_NAME):
                existing_text_object = engine.find_object(TEXT_OBJECT_NAME)
                assert isinstance(existing_text_object, Text)
                existing_text_object.text = self.text
            else:
                new_text_object = Text(self.text)
                engine.add_object(new_text_object)
        timeline.append_event(_event)


@dataclass(frozen=True)
class ResetTextCommand(Command):
    """Command to remove the text from the canvas. No-op if there is
    no text object currently present."""

    def execute(self, board: Board, timeline: TimelineLike) -> None:
        def _event(engine: 'GameEngine') -> None:
            if engine.has_object(TEXT_OBJECT_NAME):
                engine.remove_object(TEXT_OBJECT_NAME)
        timeline.append_event(_event)


@dataclass(frozen=True)
class WaitCommand(Command):
    """Command to wait silently for the specified number of frames."""
    frames: int

    def execute(self, board: Board, timeline: TimelineLike) -> None:
        timeline.wait(self.frames)


@dataclass(frozen=True)
class ChangeBackgroundCommand(Command):
    """Command to change the background image with a fade effect."""
    image_path: str

    def execute(self, board: Board, timeline: TimelineLike) -> None:
        animation_time = MOVEMENT_LENGTHS[MovementType.LONG]
        image = resolve_image_path(self.image_path)
        timeline.append_event(FadeBackgroundController.event(image, total_frames=animation_time))
        timeline.wait(animation_time)


COMMAND_REGISTRY: dict[str, type]
COMMAND_REGISTRY = {
    'move': MovePlayerCommand,
    'swap': SwapPlayerCommand,
    'add': AddPlayerCommand,
    'remove': DestroyPlayerCommand,
    'change-background': ChangeBackgroundCommand,
    'text': SetTextCommand,
    'hide-text': ResetTextCommand,
    'wait': WaitCommand,
}


def parse_command(command_sexpr: Any) -> Command:
    """Parses the S-expression-like object into an appropriate Command
    subclass.

    """
    if not isinstance(command_sexpr, list):
        raise InputParseError(f"Expected list for command, got {command_sexpr}")
    if not command_sexpr:
        raise InputParseError("Expected non-empty list for command")

    command_type = COMMAND_REGISTRY[str(command_sexpr[0])]
    return cattrs.structure_attrs_fromtuple(tuple(command_sexpr[1:]), command_type)
