from discord.ext import tasks, commands
from ..bot import Bot


class RoutineTasksCog(commands.Cog):
    """Collection of scheduled background tasks"""

    def __init__(self, bot) -> None:
        self.bot: Bot = bot
        self.clear_cache.start()
        self.media_update.start()

    def cog_unload(self):
        self.clear_cache.cancel()
        self.media_update.cancel()

    @tasks.loop(hours=1)
    async def clear_cache(self):
        self.bot.message_cache.reset()

    @tasks.loop(minutes=20)
    async def media_update(self):
        self.bot.media_tracker.update()


def setup(bot: Bot):
    bot.add_cog(RoutineTasksCog(bot))
