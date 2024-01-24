
"""Tooling for accessing the parts of the Discord API we need. Most
functionality in this module and its submodules assumes the existence
of an environment variable called DISCORD_BOT_TOKEN.

"""

from .config import get_bot_token, request_headers
from .user import User
from .cache import get_avatar


__all__ = (
    'get_bot_token', 'request_headers',
    'User',
    'get_avatar',
)
