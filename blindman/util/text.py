
from __future__ import annotations

import numpy as np
import cv2


def draw_text(
        image: np.ndarray,
        text: str,
        color: tuple[int, int, int, int] = (0, 0, 0, 0),
        font_scale: float = 1.0,
        thickness: int = 1,
) -> None:
    ...
