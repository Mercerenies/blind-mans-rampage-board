
from .config import Configuration
from .engine import GameEngine
from blindman.renderer import FrameRenderer
from blindman.util import imread_rgb

import numpy as np


class GameRenderer(FrameRenderer):

    def __init__(self, config: Configuration) -> None:
        self._config = config
        self._background_image = imread_rgb(config.background_image)
        self.engine = GameEngine()

    def total_frames(self) -> int:
        return 10 * self.fps()  # Ten seconds (until we get a real calculation here)

    def fps(self) -> int:
        return self._config.fps

    def frame_size(self) -> tuple[int, int]:
        height, width, _ = self._background_image.shape
        return width, height

    def render_frame(self, frame_number: int, canvas: np.ndarray) -> None:
        # Run one step of the game engine
        self.engine.perform_step(frame_number)

        # Now draw everything
        canvas[:] = self._background_image
        self.engine.render_frame(frame_number, canvas)
