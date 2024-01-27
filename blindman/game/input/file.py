
"""The input file itself and miscellaneous helper functions and types
supporting it."""

from .config import Configuration
from blindman.game.image import resolve_image_path
from blindman.game.command import Command, parse_command
from blindman.game.object import Sprite
from blindman.game.error import InputParseError
from blindman.lisp import parse_many, Symbol

import cattrs

from dataclasses import dataclass
from typing import TextIO, Any, Mapping
from pathlib import Path


@dataclass(frozen=True)
class InputFile:
    """The full data of a .lisp input file."""

    config: Configuration
    spaces_map: dict[str, tuple[int, int]]
    objects: list['ObjectData']
    commands: list[Command]

    @classmethod
    def read_file(cls, file: str | TextIO) -> 'InputFile':
        """Reads a file or file-like object as an input file. If the
        argument is a string, it is treated as a filename. Otherwise,
        it is treated as a file-like object.

        """
        if isinstance(file, TextIO):
            file = file.read()
        else:
            file = Path(file).read_text(encoding='utf-8')
        contents = parse_many(file)
        if len(contents) < 4:
            raise InputParseError("Expecting at least 4 elements in input file")

        config = Configuration.from_sexpr(contents[0])
        spaces_map = _parse_spaces_map(contents[1])
        objects = _parse_objects(contents[2])
        commands = _parse_commands(contents[3])
        return cls(
            config=config,
            spaces_map=spaces_map,
            objects=objects,
            commands=commands,
        )


@dataclass(frozen=True)
class ObjectData:
    """Data on a single object which is initially present in the game
    room. image_path will be resolved using
    blindman.game.image.resolve_image_path and follows the same rules
    as that function's argument.

    """

    name: str
    image_path: str
    space_name: str

    @classmethod
    def from_sexpr(cls, sexpr: Any) -> 'ObjectData':
        if not isinstance(sexpr, list) or not sexpr or sexpr[0] != Symbol("object"):
            raise InputParseError("Expected (object ...) form")
        return cattrs.structure_attrs_fromtuple(tuple(sexpr[1:]), cls)

    def to_game_object(self, spaces_map: Mapping[str, tuple[int, int]]) -> Sprite:
        position = spaces_map[self.space_name]
        image = resolve_image_path(self.image_path)
        return Sprite(
            position=position,
            image=image,
            name=self.name,
        )


def _parse_spaces_map(sexpr: Any) -> dict[str, tuple[int, int]]:
    if not isinstance(sexpr, list):
        raise InputParseError("Expected a list of spaces")
    if len(sexpr) < 1 or sexpr[0] != Symbol("spaces"):
        raise InputParseError("Expected (spaces ...) form")

    entries = cattrs.structure(sexpr[1:], list[tuple[str, tuple[int, int]]])
    return {k: (v[1], v[0]) for k, v in entries}  # Load (x y) from file and store as (y, x)


def _parse_objects(sexpr: Any) -> list[ObjectData]:
    if not isinstance(sexpr, list):
        raise InputParseError("Expected a list of objects")
    if len(sexpr) < 1 or sexpr[0] != Symbol("objects"):
        raise InputParseError("Expected (objects ...) form")
    return [ObjectData.from_sexpr(x) for x in sexpr[1:]]


def _parse_commands(sexpr: Any) -> list[Command]:
    if not isinstance(sexpr, list):
        raise InputParseError("Expected a list of commands")
    if len(sexpr) < 1 or sexpr[0] != Symbol("commands"):
        raise InputParseError("Expected (commands ...) form")
    return [parse_command(x) for x in sexpr[1:]]
