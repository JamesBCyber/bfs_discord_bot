import discord
from discord.ext import commands


class BasicCommandsCog(commands.Cog):
    """Cog to setup basic input/output and cause/effect commands"""

    def __init__(self, bot) -> None:
        self.bot = bot

    @discord.slash_command(name="ping", description="FIGHT ME")
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond("Pong")


def setup(bot):
    bot.add_cog(BasicCommandsCog(bot))
