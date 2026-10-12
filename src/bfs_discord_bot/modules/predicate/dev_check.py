import discord
from discord.ext.commands import check
from ...config import settings


def is_bot_dev():
    async def predicate(ctx: discord.ApplicationContext) -> bool:
        if ctx.author.id == settings.dev_user_id:
            return True
        else:
            await ctx.respond(
                f"Please Contact the Bot Developer at <@{settings.dev_user_id}>"
            )
        return False

    return check(predicate)


def dev_bypass(ctx: discord.ApplicationContext) -> bool:
    if ctx.author.id == settings.dev_user_id:
        return True
    return False
