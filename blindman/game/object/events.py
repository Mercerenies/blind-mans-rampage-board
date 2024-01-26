
from __future__ import annotations

from .base import GameObject
from blindman.game.engine import GameEngine
from blindman.util import lerp

import numpy as np

from collections import defaultdict
from typing import Callable, Iterable

EVENT_MANAGER_NAME = '__eventmanager'

Event = Callable[[GameEngine], None]


class EventManager(GameObject):
    _name: str
    _events: dict[int, list[Event]]
    _game: GameEngine

    def __init__(self, game: GameEngine, name: str = EVENT_MANAGER_NAME) -> None:
        super().__init__()
        self._name = name
        self._events = defaultdict(list)
        self._game = game

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


def many(events: Iterable[Event]) -> Event:
    def _execute_all(game: GameEngine) -> None:
        for event in events:
            event(game)
    return _execute_all


class MoveObjectController(GameObject):

    def __init__(self, game: GameEngine, object_name: str, new_pos: tuple[int, int], total_frames: int) -> None:
        super().__init__()
        self._game = game
        self._object_name = object_name
        self._frames = 0
        self._total_frames = total_frames

        self._old_pos = game.find_object(object_name).position
        self._new_pos = new_pos

    @property
    def name(self) -> str | None:
        return None

    def step(self, frame_number: int) -> None:
        self._frames += 1
        lerp_amount = self._frames / self._total_frames
        pos_y = int(lerp(self._old_pos[0], self._new_pos[0], lerp_amount))
        pos_x = int(lerp(self._old_pos[1], self._new_pos[1], lerp_amount))
        self._game.find_object(self._object_name).position = (pos_y, pos_x)
        if self._frames >= self._total_frames:
            self._game.remove_object(self)

    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        pass  # Control object

    @classmethod
    def event(cls, object_name: str, new_pos: tuple[int, int], total_frames: int) -> Event:
        def _factory(game: GameEngine) -> MoveObjectController:
            return MoveObjectController(game, object_name, new_pos, total_frames)
        return create_object_event(_factory)
