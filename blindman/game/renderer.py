
from .input import Configuration
from .engine import GameEngine
from blindman.renderer import FrameRenderer

import numpy as np
import cv2
from attrs import define, field


@define
class GameRenderer(FrameRenderer):
    config: Configuration = field()
    engine: GameEngine = field()
    _total_frames: int = field()
    _background_image: np.ndarray = field(init=False)

    @_background_image.default
    def _background_image_default(self) -> np.ndarray:
        background_image = cv2.imread(self.config.background_image, cv2.IMREAD_UNCHANGED)
        return cv2.cvtColor(background_image, cv2.COLOR_BGRA2RGBA)

    def total_frames(self) -> int:
        return self._total_frames

    def fps(self) -> int:
        return self.config.fps

    def frame_size(self) -> tuple[int, int]:
        width, height, _ = self._background_image.shape
        return width, height

    def render_frame(self, frame_number: int, canvas: np.ndarray) -> None:
        # Run one step of the game engine
        self.engine.perform_step(frame_number)

        # Now draw everything
        canvas[:] = self._background_image
        self.engine.render_frame(frame_number, canvas)
