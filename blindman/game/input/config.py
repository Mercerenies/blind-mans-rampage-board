
from __future__ import annotations

from blindman.game.error import InputParseError
from blindman.lisp import parse_key_value_list

from dataclasses import dataclass, KW_ONLY
from typing import Any
import cattrs

DEFAULT_FPS = 60


@dataclass(frozen=True)
class Configuration:
    """Configuration for a render input file. This corresponds to the
    (configuration ...) block at the beginning of the file."""
    _: KW_ONLY
    fps: int = DEFAULT_FPS
    background_image: str
    start_space: str = "start"

    @classmethod
    def from_sexpr(cls, sexpr: Any) -> Configuration:
        """Reads an S-expression of the form (configuration :key value
        :key value ...)."""
        data_dict = parse_key_value_list(sexpr)
        if data_dict['_type'] != 'configuration':
            raise InputParseError(f'Expected a configuration S-expression, got {sexpr}')
        return cattrs.structure(data_dict, cls)
