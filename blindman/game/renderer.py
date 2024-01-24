
from .config import Configuration
from blindman.renderer import FrameRenderer

import numpy as np
import cv2


class GameRenderer(FrameRenderer):

    def __init__(self, config: Configuration) -> None:
        self._config = config
        self._background_image = cv2.imread(config.background_image)

    def total_frames(self) -> int:
        return 10 * self.fps()  # Ten seconds (until we get a real calculation here)

    def fps(self) -> int:
        return self._config.fps

    def frame_size(self) -> tuple[int, int]:
        height, width, _ = self._background_image.shape
        return width, height

    def render_frame(self, frame_number: int, canvas: np.ndarray) -> None:
        canvas[:] = self._background_image
