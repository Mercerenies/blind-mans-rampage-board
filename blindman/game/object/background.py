
from __future__ import annotations

from .base import GameObject
from .events import Event, create_object_event
from blindman.game.engine import GameEngine
from blindman.util import lerp, draw

from attrs import define, field, Attribute
import numpy as np


BACKGROUND_Z_INDEX = -100


@define(eq=False)
class FadeBackgroundController(GameObject):
    """A GameObject which interpolates a new background over time.
    This object removes itself from the room when interpolation is
    complete."""

    _game: GameEngine = field()
    image: np.ndarray = field()
    _total_frames: int = field()
    _frames: int = field(init=False, default=0)
    _alpha: float = field(init=False, default=0)

    @property
    def name(self) -> str | None:
        return None

    @property
    def z_index(self) -> int:
        return BACKGROUND_Z_INDEX

    def __attrs_pre_init__(self) -> None:
        super().__init__()

    @image.validator
    def _validate_image(self, attribute: Attribute, value: np.ndarray) -> None:
        old_background = self._game.background_image
        if old_background is None:
            # Nothing to validate
            return
        new_width, new_height, _ = value.shape
        old_width, old_height, _ = old_background.shape
        if (old_width, old_height) != (new_width, new_height):
            raise ValueError("Background image must be the same size as the old background image")

    def step(self, frame_number: int) -> None:
        self._frames += 1
        lerp_amount = self._frames / self._total_frames
        self._alpha = lerp(0, 1, lerp_amount)

        if self._frames >= self._total_frames:
            self.on_complete()
            self._game.remove_object(self)

    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        width, height, _ = self.image.shape
        draw(
            destination=canvas,
            source=self.image,
            center=(width // 2, height // 2),
            alpha=self._alpha,
        )

    def on_complete(self) -> None:
        """This method is called when the object has finished its
        fade. By default, it sets the game's background to this
        object's image. This behavior can be overridden.

        """
        self._game.background_image = self.image

    @classmethod
    def event(cls, new_image: np.ndarray, total_frames: int) -> Event:
        """An event which fades the background over time."""
        def _factory(game: GameEngine) -> FadeBackgroundController:
            return FadeBackgroundController(
                game=game,
                image=new_image,
                total_frames=total_frames,
            )
        return create_object_event(_factory)
