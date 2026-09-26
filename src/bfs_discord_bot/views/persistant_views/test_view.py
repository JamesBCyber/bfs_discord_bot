import discord
from discord import ButtonStyle, Interaction


class TestView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="test", style=ButtonStyle.grey, custom_id="testview:gray_callback"
    )
    async def gray_callback(self, button, interaction: Interaction):
        await interaction.response.send_message("Grey Clicked")

    @discord.ui.button(
        label="test", style=ButtonStyle.blurple, custom_id="testview:blurple_callback"
    )
    async def blurple_callback(self, button, interaction: Interaction):
        await interaction.response.send_message("Blurple Clicked")

    @discord.ui.button(
        label="test", style=ButtonStyle.green, custom_id="testview:green_callback"
    )
    async def green_callback(self, button, interaction: Interaction):
        await interaction.response.send_message("Green Clicked")

    @discord.ui.button(
        label="test", style=ButtonStyle.red, custom_id="testview:red_callback"
    )
    async def red_callback(self, button, interaction: Interaction):
        await interaction.response.send_message("Red Clicked")
