
from __future__ import annotations

from .base import GameObject
from blindman.game.engine import GameEngine

import numpy as np

from collections import defaultdict
from typing import Callable

EVENT_MANAGER_NAME = '__eventmanager'

GameObjectFactory = Callable[[], GameObject]


class EventManager(GameObject):
    _events: dict[int, list[GameObjectFactory]]
    _game: GameEngine

    def __init__(self, game: GameEngine, name: str = EVENT_MANAGER_NAME) -> None:
        super().__init__(name=name)
        self._events = defaultdict(list)
        self._game = game

    def append_event(self, event_time: int, event: GameObjectFactory) -> None:
        self._events[event_time].append(event)

    def step(self, frame_number: int) -> None:
        if frame_number in self._events:
            for event in self._events[frame_number]:
                new_object = event()
                self._game.add_object(new_object)

    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        pass  # EventManager is a controller object; it does not draw.
