from discord.ext import commands
import discord
import apis.sona as sonaapi
from discord import app_commands
from loguru import logger


class Sona(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="seme", description="Get a toki pona word's definition.")
    async def seme(
        self, interaction: discord.Interaction, word: str, language: str = "en"
    ):
        try:
            sona = sonaapi.get_word(word, [language])
            logger.debug(f"Successfully got definition for: {word}")
        except Exception as e:
            logger.error(e)
            error_embed = discord.Embed(
                title="Error",
                description="Word not found.",
                color=discord.Color.red(),
            )
            logger.error(f"Error getting definition for: {word}")
            await interaction.response.send_message(embed=error_embed)
            return

        sitelen_emosi = sona.representations.sitelen_emosi

        if sona.usage_category == sonaapi.UsageCategory.Core:
            color = discord.Color.green()
        elif sona.usage_category == sonaapi.UsageCategory.Common:
            color = discord.Color.blue()
        elif sona.usage_category == sonaapi.UsageCategory.Uncommon:
            color = discord.Color.orange()
        elif sona.usage_category == sonaapi.UsageCategory.Obscure:
            color = discord.Color.purple()
        else:
            color = discord.Color.from_rgb(255, 255, 255)

        embed = discord.Embed(
            title=sona.word + f" {sitelen_emosi}" if sitelen_emosi != "" else "",
            description=sona.translations[language].definition,
            color=color,
        )

        see_also = " | See also: " + ", ".join(sona.see_also)
        embed.set_footer(
            text=f"Category: {sona.usage_category.value} | Book: {sona.book.value}"
            + (see_also if sona.see_also != [] else "")
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Sona(bot))
