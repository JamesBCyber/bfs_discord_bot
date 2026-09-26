from discord.ext import tasks, commands
from ..bot import Bot


class RoutineTasksCog(commands.Cog):
    """Collection of scheduled background tasks"""

    def __init__(self, bot) -> None:
        self.bot: Bot = bot
        self.clear_cache.start()

    def cog_unload(self):
        self.clear_cache.cancel()

    @tasks.loop(hours=1)
    async def clear_cache(self):
        self.bot.message_cache.reset()


def setup(bot: Bot):
    bot.add_cog(RoutineTasksCog(bot))
