
from __future__ import annotations

from .config import Configuration
from .object import GameObject, Sprite
from blindman.lisp import parse_many, Symbol

from attrs import define, field, validators
import cv2

from dataclasses import dataclass
from typing import TextIO, Any
from pathlib import Path


@dataclass
class InputFile:
    config: Configuration
    objects: list[GameObject]

    @classmethod
    def read_file(cls, file: str | TextIO) -> InputFile:
        if isinstance(file, TextIO):
            file = file.read()
        else:
            file = Path(file).read_text(encoding='utf-8')
        contents = parse_many(file)
        if len(contents) < 2:
            raise InputParseError("Expecting at least 2 elements in input file")
        return cls(
            config=Configuration.from_sexpr(contents[0]),
            objects=_parse_objects(contents[1]),
        )


class InputParseError(Exception):
    """An error occurred while parsing a render input file."""
    pass


def _parse_objects(sexpr: Any) -> list[GameObject]:
    if not isinstance(sexpr, list):
        raise InputParseError("Expected a list of objects")
    if len(sexpr) < 1 or sexpr[0] != Symbol("objects"):
        raise InputParseError("Expected (objects ...) form")
    return [_parse_object(x) for x in sexpr[1:]]


def _validate_is_position(value: Any) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"Expected tuple, got {type(value)}")
    if len(value) != 2:
        raise TypeError(f"Expected tuple of length 2, got {value}")
    if not all(isinstance(x, int) for x in value):
        raise TypeError(f"Expected int elements in tuple, got {value}")


@define
class _ObjectData:
    name: Symbol = field(validator=validators.instance_of(Symbol))
    path: str = field(validator=validators.instance_of(str))
    position: tuple[int, int] = field(converter=tuple)

    @position.validator
    def _validate_position(self, _, value) -> None:
        _validate_is_position(value)


def _parse_object(sexpr: Any) -> GameObject:
    if not isinstance(sexpr, list) or sexpr[0] != Symbol("object"):
        raise InputParseError("Expected (object ...) form")
    if len(sexpr) != 4:
        raise InputParseError("Expected (object name path position) form")
    try:
        data = _ObjectData(*sexpr[1:])
    except TypeError as exc:
        raise InputParseError(f"Could not parse object: {exc}") from exc
    image = cv2.imread(data.path, cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    return Sprite(
        position=data.position,
        image=image,
        name=str(data.name),
    )
