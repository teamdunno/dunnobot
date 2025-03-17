import discord
from discord.ext import commands
from discord import app_commands
import apis.dicebear as db


async def style_autocomplete(interaction: discord.Interaction, current: str):
    try:
        current = current or ""  # Ensure current is a string
        return [
            app_commands.Choice(name=style, value=style)
            for style in db.ALL_STYLES
            if current in style
        ]
    except Exception as e:
        print(f"Autocomplete error: {e}")
        return []  # Return empty list to avoid breaking autocomplete


class Dicebear(commands.GroupCog, name="dicebear"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="generate", description="Generate an avatar")
    @app_commands.autocomplete(style=style_autocomplete)
    async def generate(self, interaction: discord.Interaction, seed: str, style: str):
        url = db.get_avatar_url(db.Style(style), seed)
        embed = discord.Embed(title=f"{style} on {seed}:", color=discord.Color.yellow())
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="get-styles", description="Get all available styles")
    async def get_styles(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="All available styles:",
            description="\n".join(db.ALL_STYLES),
            color=discord.Color.yellow(),
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Dicebear(bot))
