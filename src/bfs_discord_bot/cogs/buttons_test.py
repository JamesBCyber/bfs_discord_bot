import discord
from discord.ext import commands
from ..views.persistant_views import TestView


# class ButtonsCommandsCog(commands.Cog):
#     def __init__(self, bot) -> None:
#         self.bot = bot
#
#     @discord.slash_command(name="button_test", description="debug test for buttons")
#     async def ping(self, ctx: discord.ApplicationContext):
#         await ctx.respond("Pong")
#


class ViewCommandsCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @discord.slash_command(name="view_test", description="debug test for views")
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(view=TestView())


def setup(bot):
    # bot.add_cog(ButtonsCommandsCog(bot))
    bot.add_cog(ViewCommandsCog(bot))
