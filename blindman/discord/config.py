
"""Configuration accessors for Discord."""

import os

BOT_TOKEN_ENV_NAME = 'DISCORD_BOT_TOKEN'


def get_bot_token() -> str:
    """Returns the bot token, as set in the DISCORD_BOT_TOKEN
    environment variable."""
    try:
        return os.environ[BOT_TOKEN_ENV_NAME]
    except KeyError:
        raise BotTokenError(f'Could not find {BOT_TOKEN_ENV_NAME} environment variable.')


def request_headers(headers: dict[str, str] | None = None) -> dict[str, str]:
    """Builds the request headers for a Discord API request. If the
    headers parameter is passed, it is modified in-place and
    returned."""
    if headers is None:
        headers = {}
    headers['Authorization'] = f'Bot {get_bot_token()}'
    return headers


class BotTokenError(Exception):
    """Error raised if the environment variable does not exist."""
    pass
