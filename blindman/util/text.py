
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
        origin: tuple[int, int],
        *,
        align: TextAlign = TextAlign.BOTTOM_LEFT,
        font: int = cv2.FONT_HERSHEY_SIMPLEX,
        color: tuple[int, int, int, int],
        font_scale: float,
        thickness: int,
) -> None:
    """Prints a single line of text at the given position to the
    image."""
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    origin = adjust_origin(origin, (text_height, text_width), align)
    cv2.putText(image, text, (origin[1], origin[0]), font, font_scale, color, thickness)


def draw_text_multiline(
        image: np.ndarray,
        text: str,
        origin: tuple[int, int],
        *,
        align: TextAlign = TextAlign.BOTTOM_LEFT,
        font: int = cv2.FONT_HERSHEY_SIMPLEX,
        color: tuple[int, int, int, int],
        font_scale: float,
        thickness: int,
) -> None:
    """Prints newline-separated text to the given position in the
    image."""
    (_, em_height), baseline = cv2.getTextSize("M", font, font_scale, thickness)
    line_height = em_height + baseline
    lines = text.split("\n")

    # Adjust origin to start at the first line
    if align in (TextAlign.TOP_LEFT, TextAlign.TOP_CENTER, TextAlign.TOP_RIGHT):
        # Already correct
        pass
    elif align in (TextAlign.MIDDLE_LEFT, TextAlign.MIDDLE_CENTER, TextAlign.MIDDLE_RIGHT):
        origin = (origin[0] - line_height * (len(lines) - 1) // 2, origin[1])
    else:
        origin = (origin[0] - line_height * (len(lines) - 1), origin[1])

    for line in lines:
        draw_text(
            image,
            line,
            origin,
            align=align,
            font=font,
            color=color,
            font_scale=font_scale,
            thickness=thickness,
        )
        origin = (origin[0], origin[1] + line_height)


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
