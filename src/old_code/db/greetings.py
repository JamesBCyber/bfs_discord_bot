import discord
from dataclasses import dataclass
from random import choice


@dataclass
class GreetingsManager:
    greeting_map: dict[discord.Guild, Greetings]

    def __init__(self, greeting_map=None) -> None:
        if greeting_map is None:
            self.greeting_map = {}
        else:
            self.greeting_map = greeting_map

    def to_dict(self) -> dict[int, dict[str, list[str]]]:
        new_dict = {}
        for key in self.greeting_map:
            new_dict[key] = self.greeting_map[key].to_dict()
        return new_dict

    @classmethod
    async def from_dict(
        cls, data: dict[int, dict[str, list[str]]], bot: discord.Bot
    ) -> GreetingsManager:
        map = {}
        for key in data:
            guild = await bot.fetch_guild(key)
            map[guild] = Greetings.from_dict(data[key])
        return GreetingsManager(map)

    """Proxy Functions to Greetings given a Guild"""

    def add_welcome(self, guild: discord.Guild, message: str):
        self.greeting_map[guild].add_welcome(message)

    def delete_welcome(self, guild: discord.Guild, message: str):
        self.greeting_map[guild].delete_welcome(message)

    def add_remove(self, guild: discord.Guild, message: str):
        self.greeting_map[guild].add_remove(message)

    def delete_remove(self, guild: discord.Guild, message: str):
        self.greeting_map[guild].delete_remove(message)

    def add_ban(self, guild: discord.Guild, message: str):
        self.greeting_map[guild].add_ban(message)

    def delete_ban(self, guild: discord.Guild, message: str):
        self.greeting_map[guild].delete_ban(message)

    def get_random_welcome(self, guild: discord.Guild):
        return self.greeting_map[guild].get_random_welcome()

    def get_random_remove(self, guild: discord.Guild):
        return self.greeting_map[guild].get_random_remove()

    def get_random_ban(self, guild: discord.Guild):
        return self.greeting_map[guild].get_random_ban()


@dataclass
class Greetings:
    welcome_messages: list[str]
    remove_messages: list[str]
    ban_messages: list[str]

    def __init__(
        self, welcome_messages=None, remove_messages=None, ban_messages=None
    ) -> None:
        if welcome_messages is None:
            self.welcome_messages = []
        else:
            self.welcome_messages = welcome_messages

        if remove_messages is None:
            self.remove_messages = []
        else:
            self.remove_messages = remove_messages

        if ban_messages is None:
            self.ban_messages = []
        else:
            self.ban_messages = ban_messages

    def to_dict(self) -> dict[str, list[str]]:
        return {
            "welcome_messages": self.welcome_messages,
            "remove_messages": self.remove_messages,
            "ban_messages": self.ban_messages,
        }

    @classmethod
    def from_dict(cls, data: dict[str, list[str]]) -> Greetings:
        return cls(
            welcome_messages=data["welcome_messages"],
            remove_messages=data["remove_messages"],
            ban_messages=data["ban_messages"],
        )

    def add_welcome(self, message: str):
        self.welcome_messages.append(message)

    def delete_welcome(self, message: str):
        self.welcome_messages.remove(message)

    def add_remove(self, message: str):
        self.remove_messages.append(message)

    def delete_remove(self, message: str):
        self.remove_messages.remove(message)

    def add_ban(self, message: str):
        self.ban_messages.append(message)

    def delete_ban(self, message: str):
        self.ban_messages.remove(message)

    def get_random_welcome(self):
        return choice(self.welcome_messages)

    def get_random_remove(self):
        return choice(self.remove_messages)

    def get_random_ban(self):
        return choice(self.ban_messages)
