import json
from typing import TYPE_CHECKING, Any

import discord

if TYPE_CHECKING:
    from .guild_data import Guilds
from .wrapper import save_method


class ChannelData:
    """Tracks a Guilds various channels

    Log, Media (to post updates to), Commands (if restircting command use)
    """

    KEY = "channels"
    LOG_KEY = "log"  # int
    MEDIA_KEY = "media"  # int
    COMMANDS_KEY = "commands"  # int

    _root: Guilds
    _log: discord.TextChannel | None
    _media: discord.TextChannel | None
    _commands: discord.TextChannel | None

    def __str__(self) -> str:
        string = ""
        string += (
            f"Logs:{self._log.name}\nLogs ID:{self._log.id}\n" if self._log else ""
        )
        string += (
            f"Media:{self._media.name}\nMedia ID:{self._media.id}\n"
            if self._media
            else ""
        )
        string += (
            f"Commands:{self._commands.name}\nCommands ID:{self._commands.id}"
            if self._commands
            else ""
        )
        return string

    def __init__(
        self,
        root: Guilds,
        log: discord.TextChannel | None = None,
        media: discord.TextChannel | None = None,
        commands: discord.TextChannel | None = None,
    ) -> None:
        self._root = root
        self._log = log
        self._media = media
        self._commands = commands

    @property
    def log(self):
        return self._log

    @save_method
    def set_log_channel(self, log: discord.TextChannel):
        if isinstance(log, discord.TextChannel):
            self._log = log

    @property
    def media(self):
        return self._media

    @save_method
    def set_media_channel(self, media: discord.TextChannel):
        if isinstance(media, discord.TextChannel):
            self._media = media

    @property
    def commands(self):
        return self._commands

    @save_method
    def set_commands_channel(self, commands: discord.TextChannel):
        if isinstance(commands, discord.TextChannel):
            self._commands = commands

    def to_dict(self) -> dict[str, Any]:
        data = {}
        if self._log:
            data[self.LOG_KEY] = self._log.id
        if self._media:
            data[self.MEDIA_KEY] = self._media.id
        if self._commands:
            data[self.COMMANDS_KEY] = self._commands.id
        return data

    @classmethod
    async def from_json(
        cls,
        root: Guilds,
        guild: discord.Guild,
        data: dict[str, int],
        string: str | None = None,
    ) -> ChannelData:
        if string:
            data = json.loads(string)

        log = None
        if log_id := data.get(cls.LOG_KEY):
            tmp_channel = await guild.fetch_channel(log_id)
            if isinstance(tmp_channel, discord.TextChannel):
                log = tmp_channel

        media = None
        if media_id := data.get(cls.MEDIA_KEY):
            tmp_channel = await guild.fetch_channel(media_id)
            if isinstance(tmp_channel, discord.TextChannel):
                media = tmp_channel

        commands = None
        if commands_id := data.get(cls.COMMANDS_KEY):
            tmp_channel = await guild.fetch_channel(commands_id)
            if isinstance(tmp_channel, discord.TextChannel):
                commands = tmp_channel

        # assume all are TextChannels, should actually be validated in the slash command to register the channel
        # reading from database will always contain valid data if used properly
        return cls(
            root=root,
            log=log,
            media=media,
            commands=commands,
        )
