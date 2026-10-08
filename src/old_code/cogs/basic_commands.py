import discord
from discord.ext import commands


class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(
            discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long)
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])


class BasicCommandsCog(commands.Cog):
    """Cog to setup basic input/output and cause/effect commands"""

    def __init__(self, bot) -> None:
        self.bot = bot

    @discord.slash_command(name="ping", description="FIGHT ME")
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond("Pong")

    @discord.slash_command(name="modal_test")
    async def modal_slash(self, ctx: discord.ApplicationContext):
        """Shows an example of a modal dialog being invoked from a slash command."""
        modal = MyModal(title="Modal via Slash Command")
        await ctx.send_modal(modal)


def setup(bot):
    bot.add_cog(BasicCommandsCog(bot))
