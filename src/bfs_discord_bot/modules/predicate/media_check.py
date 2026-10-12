import discord
from discord.ext.commands import check
from ...config import settings
from .dev_check import dev_bypass


def has_media_role():
    async def predicate(ctx: discord.ApplicationContext) -> bool:
        if dev_bypass(ctx):
            return True

        media_roles = ctx.bot.guilds[ctx.guild].media_roles
        has_role = any(role in  for role in ctx.author.roles)

    return check(predicate)
