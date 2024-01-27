
from blindman.discord import get_avatar

import cv2
import numpy as np

DISCORD_AVATAR_SIZE = 32


def resolve_image_path(image_path: str) -> np.ndarray:
    """Load the image at the given path as a numpy array.

    If the path starts with "discord:", then it is read as a Discord
    user ID and loads the avatar for the given Discord user. In that
    case, the DISCORD_BOT_TOKEN environment variable must be set.

    In any other case, the path is treated as a file path on the local
    file system.

    """
    if image_path.startswith('discord:'):
        return _load_discord_image(image_path[8:])
    else:
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
        return image


def _load_discord_image(user_id: str) -> np.ndarray:
    avatar_bytes = get_avatar(user_id, size=DISCORD_AVATAR_SIZE)
    image = cv2.imdecode(np.frombuffer(avatar_bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    return image
