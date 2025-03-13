from discord.ext import commands
from discord import app_commands
import discord

import apis.xkcd as xkcdapi


class Xkcd(commands.GroupCog, name="xkcd"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="current", description="Get the current XKCD comic.")
    async def current_xkcd(self, interaction: discord.Interaction):
        current_comic = xkcdapi.get_current_comic()
        embed = discord.Embed(
            title=current_comic.title,
            description=current_comic.alt,
            color=discord.Color.from_rgb(255, 255, 255),
        )
        embed.set_image(url=current_comic.img)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="specific", description="Get a specific XKCD comic by number."
    )
    async def specific_xkcd(self, interaction: discord.Interaction, comic_number: int):
        comic = xkcdapi.get_comic(comic_number)
        embed = discord.Embed(
            title=comic.title,
            description=comic.alt,
            color=discord.Color.from_rgb(255, 255, 255),
        )
        embed.set_image(url=comic.img)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Xkcd(bot))
