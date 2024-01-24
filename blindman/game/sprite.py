
from .engine import GameObject

import numpy as np


class Sprite(GameObject):
    image: np.ndarray
    position: tuple[int, int]

    def __init__(self, x: int, y: int, image: np.ndarray, name: str | None = None) -> None:
        super().__init__(name=name)
        self.image = image
        self.position = (x, y)

    def step(self, frame_number: int) -> None:
        pass  # Sprites are static objects; they do not move on their own

    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        ...
