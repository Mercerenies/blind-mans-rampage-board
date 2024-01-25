
from .config import Configuration
from .object import GameObject, Sprite
from .error import InputParseError
from blindman.lisp import parse_many, Symbol

import cattrs
import cv2

from dataclasses import dataclass
from typing import TextIO, Any
from pathlib import Path


@dataclass(frozen=True)
class InputFile:
    config: Configuration
    spaces_map: dict[str, tuple[int, int]]
    objects: list['ObjectData']

    @classmethod
    def read_file(cls, file: str | TextIO) -> 'InputFile':
        if isinstance(file, TextIO):
            file = file.read()
        else:
            file = Path(file).read_text(encoding='utf-8')
        contents = parse_many(file)
        if len(contents) < 3:
            raise InputParseError("Expecting at least 3 elements in input file")

        config = Configuration.from_sexpr(contents[0])
        spaces_map = _parse_spaces_map(contents[1])
        objects = _parse_objects(contents[2])
        return cls(
            config=config,
            spaces_map=spaces_map,
            objects=objects,
        )


@dataclass(frozen=True)
class ObjectData:
    name: str
    image_path: str
    position: tuple[int, int]

    @classmethod
    def from_sexpr(cls, sexpr: Any) -> 'ObjectData':
        if not isinstance(sexpr, list) or not sexpr or sexpr[0] != Symbol("object"):
            raise InputParseError("Expected (object ...) form")
        return cattrs.structure_attrs_fromtuple(tuple(sexpr[1:]), cls)

    def to_game_object(self) -> GameObject:
        image = cv2.imread(self.image_path, cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        return Sprite(
            position=self.position,
            image=image,
            name=self.name,
        )


def _parse_spaces_map(sexpr: Any) -> dict[str, tuple[int, int]]:
    if not isinstance(sexpr, list):
        raise InputParseError("Expected a list of spaces")
    if len(sexpr) < 1 or sexpr[0] != Symbol("spaces"):
        raise InputParseError("Expected (spaces ...) form")

    entries = cattrs.structure(sexpr[1:], list[tuple[str, tuple[int, int]]])
    return dict(entries)


def _parse_objects(sexpr: Any) -> list[ObjectData]:
    if not isinstance(sexpr, list):
        raise InputParseError("Expected a list of objects")
    if len(sexpr) < 1 or sexpr[0] != Symbol("objects"):
        raise InputParseError("Expected (objects ...) form")
    return [ObjectData.from_sexpr(x) for x in sexpr[1:]]
