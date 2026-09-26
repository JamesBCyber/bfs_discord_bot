import os
import discord
from discord.ext import commands
from .config import settings
from .bot import Bot


def main() -> None:
    intents = discord.Intents.all()
    bot = Bot(intents=intents)

    for filename in os.listdir("./src/bfs_discord_bot/cogs/"):
        if filename.endswith(".py"):
            extension_name = f"bfs_discord_bot.cogs.{filename[:-3]}"
            try:
                bot.load_extension(extension_name)
                print(f"Loaded extension: {extension_name}")
            except Exception as err:
                print(f"Failed to load extension {extension_name}: {err}")
    bot.run(settings.discord_token)
