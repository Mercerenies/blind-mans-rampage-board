
from __future__ import annotations

from blindman.lisp import Symbol

from dataclasses import dataclass, KW_ONLY
from typing import Any, Optional

DEFAULT_FPS = 60


@dataclass(frozen=True)
class Configuration:
    """Configuration for a render input file."""
    _: KW_ONLY
    fps: int = DEFAULT_FPS
    background_image: str

    @classmethod
    def from_sexpr(cls, sexpr: Any) -> Configuration:
        fps = DEFAULT_FPS
        background_image: Optional[str] = None

        if not isinstance(sexpr, list) or not sexpr or sexpr[0] != Symbol('configuration'):
            raise ConfigurationParseError('Expected a configuration S-expression')
        if len(sexpr) % 2 == 0:
            raise ConfigurationParseError('Expected an even number of arguments')

        for i in range(1, len(sexpr), 2):
            key = sexpr[i]
            value = sexpr[i + 1]
            match key:
                case Symbol(':fps'):
                    if not isinstance(value, int):
                        raise ConfigurationParseError(f'Expected an integer for :fps, got {value}')
                    fps = value
                case Symbol(':background-image'):
                    if not isinstance(value, str):
                        raise ConfigurationParseError(f'Expected a string for :background-image, got {value}')
                    background_image = value
                case _:
                    raise ConfigurationParseError(f'Unexpected configuration argument {key}')

        if background_image is None:
            raise ConfigurationParseError('Missing :background-image argument')
        return cls(fps=fps, background_image=background_image)


class ConfigurationParseError(Exception):
    """An error occurred while parsing a render input file."""
    pass
