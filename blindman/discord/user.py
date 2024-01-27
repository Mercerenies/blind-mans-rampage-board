
from __future__ import annotations

from .config import request_headers

from attrs import define, field, validators
import cattrs
import requests


@define(frozen=True)
class User:
    id: str = field(validator=validators.instance_of(str))
    username: str = field(validator=validators.instance_of(str))
    avatar: str = field(validator=validators.instance_of(str))
    discriminator: str = field(validator=validators.instance_of(str))

    @classmethod
    def get(cls, user_id: str) -> User:
        resp = requests.get(f"https://discord.com/api/v10/users/{user_id}", headers=request_headers())
        resp.raise_for_status()
        return cattrs.structure(resp.json(), cls)

    def avatar_url(self, size: int | None = None) -> str:
        url = f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png"
        if size is not None:
            url += f"?size={size}"
        return url

    def get_avatar(self, size: int | None = None) -> bytes:
        resp = requests.get(self.avatar_url(size=size))
        resp.raise_for_status()
        return resp.content
