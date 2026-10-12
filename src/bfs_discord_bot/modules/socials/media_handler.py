import json

import discord

from .youtube import YoutubeChannel

DEFAULT_JSON_FILENAME = "media.json"


class MediaHandler:
    _youtube: set[YoutubeChannel]

    def __init__(self, filename: str = DEFAULT_JSON_FILENAME) -> None:
        pass

    def save(self):
        pass

    @classmethod
    def load(
        cls, bot: discord.Bot, filename: str = DEFAULT_JSON_FILENAME
    ) -> MediaHandler:
        pass
