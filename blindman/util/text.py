
from __future__ import annotations

import numpy as np
import cv2

from enum import Enum, auto


class TextAlign(Enum):
    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()
    MIDDLE_LEFT = auto()
    MIDDLE_CENTER = auto()
    MIDDLE_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_CENTER = auto()
    BOTTOM_RIGHT = auto()


def draw_text(
        image: np.ndarray,
        text: str,
        origin: tuple[int, int],  # (height, width)
        *,
        align: TextAlign = TextAlign.BOTTOM_LEFT,
        font: int = cv2.FONT_HERSHEY_SIMPLEX,
        color: tuple[int, int, int, int],
        font_scale: float,
        thickness: int,
) -> None:
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    origin = adjust_origin(origin, (text_height, text_width), align)
    cv2.putText(image, text, (origin[1], origin[0]), font, font_scale, color, thickness)


def adjust_origin(origin: tuple[int, int], text_box: tuple[int, int], alignment: TextAlign) -> tuple[int, int]:
    text_height, text_width = text_box
    origin_y, origin_x = origin
    match alignment:
        case TextAlign.TOP_LEFT:
            origin_y -= text_height
        case TextAlign.TOP_CENTER:
            origin_x -= text_width // 2
            origin_y -= text_height
        case TextAlign.TOP_RIGHT:
            origin_x -= text_width
            origin_y -= text_height
        case TextAlign.MIDDLE_LEFT:
            origin_y -= text_height // 2
        case TextAlign.MIDDLE_CENTER:
            origin_x -= text_width // 2
            origin_y -= text_height // 2
        case TextAlign.MIDDLE_RIGHT:
            origin_x -= text_width
            origin_y -= text_height // 2
        case TextAlign.BOTTOM_LEFT:
            pass  # cv2 default behavior
        case TextAlign.BOTTOM_CENTER:
            origin_x -= text_width // 2
        case TextAlign.BOTTOM_RIGHT:
            origin_x -= text_width
    return origin_y, origin_x
