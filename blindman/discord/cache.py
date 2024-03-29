
"""Caching for user avatars, so we don't constantly ping Discord's
server.

This cache uses a local Redis data store which tracks avatars by their
user and requested size parameter. If Redis is not running, then
get_avatar is equivalent to simply querying the Discord API every time
(that is, no caching is performed). In that case, loading this module
will print a warning. The warning can be suppressed by setting the
NO_REDIS environment variable.

"""

from .user import User

import redis

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

REDIS_KEY = "blindman"
NO_REDIS_FLAG = 'NO_REDIS'


_LOCAL_REDIS: redis.Redis | None
_LOCAL_REDIS = redis.Redis()

if not _LOCAL_REDIS.ping():
    _LOCAL_REDIS = None
    if not os.environ.get(NO_REDIS_FLAG):
        logger.warning("Redis is not running. No cache will be available.")
        logger.warning(f"Install redis or set the environment variable {NO_REDIS_FLAG} to suppress this message.")


def get_avatar(user_id: str, size: int | None = None) -> bytes:
    """Returns the avatar for the given user in the given size. This
    function uses a Redis cache if available but falls back to a
    direct Discord API call if needed.

    """
    cache_key = f"avatar:{user_id}?size={size}"
    if _LOCAL_REDIS:
        cached_value: Any = _LOCAL_REDIS.hget(REDIS_KEY, cache_key)  # Any: Redis type is wrong
        if cached_value:
            return cached_value

    user = User.get(user_id)
    avatar = user.get_avatar(size=size)
    if _LOCAL_REDIS:
        _LOCAL_REDIS.hset(REDIS_KEY, cache_key, avatar)  # type: ignore # Redis type is wrong
    return avatar
