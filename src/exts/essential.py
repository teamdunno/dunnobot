from discord.ext import commands
from discord import app_commands
from loguru import logger
import discord


class Essential(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check if the bot is online.")
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Pong!",
            description="The bot is working fine!",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug("Syncing commands...")
        await self.bot.tree.sync()
        logger.debug("Commands synced!")
        logger.info(f"Logged in as {self.bot.user.name} ({self.bot.user.id})")


async def setup(bot: commands.Bot):
    await bot.add_cog(Essential(bot))
