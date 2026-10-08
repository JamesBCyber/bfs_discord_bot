import discord
from discord.ext import commands


class GreetingsCog(commands.Cog):
    """Manages all the greetings commands for welcome, goodbye, and ban messages"""

    greetings = discord.SlashCommandGroup("greetings")

    def __init__(self, bot) -> None:
        self.bot = bot

    @greetings.command(name="add_welcome", description="Add a welcome message template")
    async def add_welcome(self, ctx: discord.ApplicationContext):
        guild = ctx.guild
        bot.

    @greetings.command(
        name="delete_welcome", description="Deletes a welcome message template"
    )
    async def delete_welcome(self, ctx: discord.ApplicationContext):
        await ctx.respond("Pong")


def setup(bot):
    bot.add_cog(GreetingsCog(bot))
