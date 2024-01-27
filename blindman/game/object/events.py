
from __future__ import annotations

from .base import GameObject
from .sprite import Sprite
from blindman.game.engine import GameEngine
from blindman.util import lerp

from attrs import define, field
import numpy as np

from collections import defaultdict
from typing import Callable, Iterable

EVENT_MANAGER_NAME = '__eventmanager'

Event = Callable[[GameEngine], None]


@define(eq=False)
class EventManager(GameObject):
    _game: GameEngine = field()
    _name: str = field(default=EVENT_MANAGER_NAME)
    _events: dict[int, list[Event]] = field(init=False, factory=lambda: defaultdict(list))

    def __attrs_pre_init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str:
        return self._name

    def append_event(self, event_time: int, event: Event) -> None:
        self._events[event_time].append(event)

    def step(self, frame_number: int) -> None:
        if frame_number in self._events:
            for event in self._events[frame_number]:
                event(self._game)

    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        pass  # EventManager is a controller object; it does not draw.


def create_object_event(object_factory: Callable[[GameEngine], GameObject]) -> Event:
    def _event(game: GameEngine) -> None:
        game.add_object(object_factory(game))
    return _event


def destroy_object_event(object_name: str) -> Event:
    def _event(game: GameEngine) -> None:
        game.remove_object(object_name)
    return _event


def many(events: Iterable[Event]) -> Event:
    def _execute_all(game: GameEngine) -> None:
        for event in events:
            event(game)
    return _execute_all


@define(eq=False)
class MoveObjectController(GameObject):
    _game: GameEngine
    _object_name: str
    _new_pos: tuple[int, int]
    _total_frames: int

    _frames: int = field(init=False, default=0)
    _old_pos: tuple[int, int] = field(init=False)

    @_old_pos.default
    def _old_pos_default(self) -> tuple[int, int]:
        target = self._game.find_object(self._object_name)
        assert isinstance(target, Sprite)
        return target.position

    def __attrs_pre_init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str | None:
        return None

    def step(self, frame_number: int) -> None:
        self._frames += 1
        lerp_amount = self._frames / self._total_frames
        pos_y = int(lerp(self._old_pos[0], self._new_pos[0], lerp_amount))
        pos_x = int(lerp(self._old_pos[1], self._new_pos[1], lerp_amount))

        target = self._game.find_object(self._object_name)
        assert isinstance(target, Sprite)

        target.position = (pos_y, pos_x)
        if self._frames >= self._total_frames:
            self._game.remove_object(self)

    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        pass  # Control object

    @classmethod
    def event(cls, object_name: str, new_pos: tuple[int, int], total_frames: int) -> Event:
        def _factory(game: GameEngine) -> MoveObjectController:
            return MoveObjectController(game, object_name, new_pos, total_frames)
        return create_object_event(_factory)
