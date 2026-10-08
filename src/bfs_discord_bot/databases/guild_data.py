import discord
import json
from typing import Any


class GuildData:
    GUILD_ID = "guild_id"  # int
    CHANNEL_LOG = "channel_log"  # int
    CHANNEL_MEDIA = "channel_media"  # int
    CHANNEL_COMMANDS = "channel_commands"  # int
    """
    ```json
    {
        "guild_id": int
        "channel_log": int,
        "channel_media": int,
        "channel_commands": int,
    }
    ```
    """

    guild: discord.Guild
    id: int
    channel_log: discord.TextChannel | None
    channel_media: discord.TextChannel | None
    channel_commands: discord.TextChannel | None

    def __init__(
        self,
        guild: discord.Guild | None = None,
        guild_id: int | None = None,
        channel_log: discord.TextChannel | None = None,
        channel_media: discord.TextChannel | None = None,
        channel_commands: discord.TextChannel | None = None,
    ) -> None:
        pass

    def to_dict(self) -> dict[str, Any]:
        data = {self.GUILD_ID: self.guild.id}

        if self.channel_log:
            data[self.CHANNEL_LOG] = self.channel_log.id

        if self.channel_media:
            data[self.CHANNEL_MEDIA] = self.channel_media.id

        if self.channel_commands:
            data[self.CHANNEL_COMMANDS] = self.channel_commands.id

        return data

    @classmethod
    async def from_json(
        cls, guild: discord.Guild, data: dict[str, int], string: str | None = None
    ) -> GuildData:
        if string:
            data = json.loads(string)

        log = None
        if log_id := data.get(cls.CHANNEL_LOG):
            log = await guild.fetch_channel(log_id)

        media = None
        if media_id := data.get(cls.CHANNEL_MEDIA):
            media = await guild.fetch_channel(media_id)

        commands = None
        if commands_id := data.get(cls.CHANNEL_COMMANDS):
            commands = await guild.fetch_channel(commands_id)

        guild_data = cls(
            guild=guild,
            guild_id=guild.id,
            channel_log=log,
            channel_media=media,
            channel_commands=commands,
        )
        return guild_data


class Guilds:
    """Init once and use same reference

    Data is stored in a json file with id's and on class.load() fetches all data needed
    """

    _filename: str
    _guilds: dict[discord.Guild, GuildData]

    def __init__(self, filename: str = "guilds.json") -> None:
        self.filename = filename

    def _save(self) -> None:
        pass

    @classmethod
    async def load(cls, bot: discord.Bot, filename: str = "guilds.json") -> Guilds:
        guilds = cls(filename=filename)

        with open(filename) as f:
            data = json.load(f)

        for key in data:
            guild = await bot.fetch_guild(key)
            gd = GuildData.from_json(guild=guild, data=data[key])

        return guilds

    def add_entry(self, guild: discord.Guild, guild_data: GuildData):
        self._guilds[guild] = guild_data
