
"""Defines the User class."""

from __future__ import annotations

from .config import request_headers

from attrs import define, field, validators
import cattrs
import requests


@define(frozen=True)
class User:
    """A Discord user."""

    id: str = field(validator=validators.instance_of(str))
    username: str = field(validator=validators.instance_of(str))
    avatar: str = field(validator=validators.instance_of(str))
    discriminator: str = field(validator=validators.instance_of(str))

    @classmethod
    def get(cls, user_id: str) -> User:
        """Get a user's information from Discord, from their ID.
        Raises requests.HTTPError if the user does not exist."""
        resp = requests.get(f"https://discord.com/api/v10/users/{user_id}", headers=request_headers())
        resp.raise_for_status()
        return cattrs.structure(resp.json(), cls)

    def avatar_url(self, size: int | None = None) -> str:
        """Returns a URL at cdn.discordapp.com at which the user's
        avatar can be accessed.

        """
        url = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png"
        if size is not None:
            url += f"?size={size}"
        return url

    def get_avatar(self, size: int | None = None) -> bytes:
        """Gets the user's current avatar (as a byte stream)."""
        resp = requests.get(self.avatar_url(size=size))
        resp.raise_for_status()
        return resp.content
