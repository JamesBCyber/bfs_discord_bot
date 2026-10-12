import asyncio
import json
from typing import Any

import discord

from .channels import ChannelData
from .roles import RoleData
from .wrapper import save_method

DEFAULT_JSON_FILENAME = "guilds.json"


class GuildData:
    """Internal Guild Data, Refer to ChannelData and RoleData for accessing relevant data"""

    GUILD_ID_KEY = "guild_id"  # int

    _root: Guilds
    guild: discord.Guild
    channels: ChannelData
    roles: RoleData

    def __str__(self) -> str:
        return (
            f"Guild:{self.guild.name}\nID:{self.guild.id}"
            "\n" + str(self.channels) + "\n" + str(self.roles)
        )

    def __init__(
        self,
        root: Guilds,
        guild: discord.Guild,
        channels: ChannelData,
        roles: RoleData,
    ) -> None:
        self._root = root
        self.guild = guild
        self.channels = channels
        self.roles = roles

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        data[self.GUILD_ID_KEY] = self.guild.id
        data[self.channels.KEY] = self.channels.to_dict()
        data[self.roles.KEY] = self.roles.to_dict()
        return data

    @classmethod
    async def from_json(
        cls,
        root: Guilds,
        bot: discord.Bot,
        data: dict[str, Any] | None = None,
        string: str | None = None,
    ) -> GuildData:
        if string:
            data = json.loads(string)

        # Expect at either data or string, if neither, error
        if data is None:
            raise ValueError

        guild = await bot.fetch_guild(data[cls.GUILD_ID_KEY])

        channel_data = await ChannelData.from_json(
            root=root, guild=guild, data=data[ChannelData.KEY]
        )
        role_data = await RoleData.from_json(
            root=root, guild=guild, data=data[RoleData.KEY]
        )

        guild_data = cls(
            root=root,
            guild=guild,
            channels=channel_data,
            roles=role_data,
        )
        return guild_data


class Guilds:
    """Init once and use same reference

    Data is stored in a json file with id's and on class.load() fetches all data needed
    """

    filename: str
    guilds: dict[discord.Guild, GuildData]

    def __init__(self, filename: str = DEFAULT_JSON_FILENAME) -> None:
        self.filename = filename
        self.guilds = {}

    def __getitem__(self, value: discord.Guild) -> GuildData:
        return self.guilds.get(value)

    def save(self) -> None:
        data = {}
        for k, v in self.guilds.items():
            data[k.id] = v.to_dict()
        with open(self.filename, "w") as f:
            json.dump(data, f)

    @classmethod
    async def load(
        cls, bot: discord.Bot, filename: str = DEFAULT_JSON_FILENAME
    ) -> Guilds:
        guilds = cls(filename=filename)

        with open(filename) as f:
            data = json.load(f)

        guild_values, guild_datas = await asyncio.gather(
            asyncio.gather(*[bot.fetch_guild(key) for key in data]),
            asyncio.gather(
                *[
                    GuildData.from_json(root=guilds, bot=bot, data=data[key])
                    for key in data
                ]
            ),
        )
        for guild, data in zip(guild_values, guild_datas):
            guilds.add_entry(guild, data)

        return guilds

    def add_entry(self, guild: discord.Guild, guild_data: GuildData):
        self.guilds[guild] = guild_data
