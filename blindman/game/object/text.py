
from .base import GameObject

import numpy as np
import cv2


TEXT_OBJECT_NAME = "__text"


class Text(GameObject):

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    @property
    def name(self) -> str:
        return TEXT_OBJECT_NAME

    def step(self, frame_number: int) -> None:
        pass  # Status text is a static object; it does not move on its own

    def draw(self, frame_number: int, canvas: np.ndarray) -> None:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (0, 0, 0, 255)
        thickness = 2
        (text_width, _), _ = cv2.getTextSize(self.text, font, font_scale, thickness)
        display_height, display_width, _ = canvas.shape
        pos = ((display_width - text_width) // 2, display_height - 32)
        cv2.putText(canvas, self.text, pos, font, font_scale, color, thickness)
