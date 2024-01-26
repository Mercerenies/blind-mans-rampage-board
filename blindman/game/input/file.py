
from .config import Configuration
from blindman.game.command import Command, parse_command
from blindman.game.object import Sprite
from blindman.game.error import InputParseError
from blindman.lisp import parse_many, Symbol
from blindman.discord import get_avatar

import cattrs
import cv2
import numpy as np

from dataclasses import dataclass
from typing import TextIO, Any, Mapping
from pathlib import Path


DISCORD_AVATAR_SIZE = 32


@dataclass(frozen=True)
class InputFile:
    config: Configuration
    spaces_map: dict[str, tuple[int, int]]
    objects: list['ObjectData']
    commands: list[Command]

    @classmethod
    def read_file(cls, file: str | TextIO) -> 'InputFile':
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


def resolve_image_path(image_path: str) -> np.ndarray:
    if image_path.startswith('discord:'):
        return _load_discord_image(image_path[8:])
    else:
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        return image


def _load_discord_image(user_id: str) -> np.ndarray:
    avatar_bytes = get_avatar(user_id, size=DISCORD_AVATAR_SIZE)
    image = cv2.imdecode(np.frombuffer(avatar_bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    return image


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
