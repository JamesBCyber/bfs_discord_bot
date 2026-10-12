import asyncio
import json
from typing import TYPE_CHECKING, Any

import discord

if TYPE_CHECKING:
    from .guild_data import Guilds
from .wrapper import save_method


class RoleData:
    """Tracks a Guilds Role data, useful for both authorization and pings"""

    KEY = "roles"
    MEDIA_KEY = "media"  # set[int]
    MEDIA_PINGS_KEY = "media_pings"  # int

    _root: Guilds
    _media: set[discord.Role]
    _media_ping: discord.Role | None

    def __str__(self) -> str:
        string = ""
        string += f"Media Managers: {self._media}\n"
        string += f"Media Pings: {self._media_ping}" if self._media_ping else ""
        return string

    def __init__(
        self,
        root: Guilds,
        media_roles: set[discord.Role] | None = None,
        media_ping: discord.Role | None = None,
    ) -> None:
        self._root = root
        self._media = media_roles if media_roles else set()
        self._media_ping = media_ping

    @property
    def media(self):
        return self._media

    @save_method
    def add_media_manager(self, role: discord.Role):
        if isinstance(role, discord.Role):
            self._media.add(role)

    @save_method
    def remove_media_manager(self, role: discord.Role):
        if isinstance(role, discord.Role):
            self._media.remove(role)

    @property
    def media_ping(self):
        return self._media_ping

    @save_method
    def set_media_ping(self, role: discord.Role):
        if isinstance(role, discord.Role):
            self._media_ping = role

    def to_dict(self) -> dict[str, Any]:
        data = {}

        if self._media:
            data[self.MEDIA_KEY] = [role.id for role in self._media]
        if self._media_ping:
            data[self.MEDIA_PINGS_KEY] = self._media_ping.id

        return data

    @classmethod
    async def from_json(
        cls,
        root: Guilds,
        guild: discord.Guild,
        data: dict[str, Any],
        string: str | None = None,
    ) -> RoleData:
        if string:
            data = json.loads(string)

        media = None
        if media_roles := data.get(cls.MEDIA_KEY):
            # New
            tasks = [guild.fetch_role(role_id) for role_id in media_roles]
            media = {
                role
                for role in await asyncio.gather(*tasks)
                if isinstance(role, discord.Role)
            }

        media_ping = None
        if media_ping_id := data.get(cls.MEDIA_PINGS_KEY):
            tmp_role = await guild.fetch_role(media_ping_id)
            if isinstance(tmp_role, discord.Role):
                media_ping = tmp_role

        return cls(root=root, media_roles=media, media_ping=media_ping)
