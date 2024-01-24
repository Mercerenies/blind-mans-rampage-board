
import os

BOT_TOKEN_ENV_NAME = 'DISCORD_BOT_TOKEN'


def get_bot_token() -> str:
    try:
        return os.environ[BOT_TOKEN_ENV_NAME]
    except KeyError:
        raise BotTokenError(f'Could not find {BOT_TOKEN_ENV_NAME} environment variable.')


def request_headers(headers: dict[str, str] | None = None) -> dict[str, str]:
    if headers is None:
        headers = {}
    headers['Authorization'] = f'Bot {get_bot_token()}'
    return headers


class BotTokenError(Exception):
    pass
