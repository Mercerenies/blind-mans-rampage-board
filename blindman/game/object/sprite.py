
from .base import GameObject
from blindman.util import draw

from attrs import define, field
import numpy as np


@define(eq=False)
class Sprite(GameObject):
    """A sprite which draws itself centered at the given position. The
    position and alpha value are mutable, which can be used to animate
    the sprite."""

    position: tuple[int, int]
    image: np.ndarray
    _name: str
    alpha: float = field(default=1.0, converter=float)

    def __attrs_pre_init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str:
        return self._name

    def step(self, frame_number: int) -> None:
        pass  # Sprites are static objects; they do not move on their own

    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        draw(canvas, self.image, self.position, alpha=self.alpha)
