import discord
from discord.ext import commands
from discord import app_commands
import pollinations as ai

SYSTEM_PROMPT = """
You are a helpful assistant named DunnoBot. Your instructions are as follows:

- Your pronouns are he/him.
- Answer user questions as helpfully as possible
- Answer user questions concisely, simply and efficently
- Do NOT ask the user if they have any other inqueries, instead
  simply answer any questions they might have in the text you shall
  output
"""


class Pollinations(commands.GroupCog, name="ai"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="text", description="Generate text")
    async def text(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()

        text = ai.Async.Text(
            model=ai.Async.Text.openai(),
            system=SYSTEM_PROMPT,
            contextual=True,
            messages=[],
            seed="random",
            jsonMode=False,
            referrer="pollinations.py",
        )

        res = await text(prompt, encode=True, display=False)

        embed = discord.Embed(
            title="",
            description=res.response,
            color=discord.Color.yellow(),
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="image", description="Generate an image")
    async def image(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()

        model = ai.Async.Image(nologo=True)

        res = await model(prompt)

        embed = discord.Embed(color=discord.Color.yellow())

        embed.set_image(url=res.response.response.url)

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Pollinations(bot))
