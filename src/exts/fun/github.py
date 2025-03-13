from discord.ext import commands
from loguru import logger
from discord import app_commands
import discord
import apis.github as ghapi


class Github(commands.GroupCog, name="gh"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="repo", description="Get information about a GitHub repository."
    )
    async def gh_repo(self, interaction: discord.Interaction, repo: str):
        try:
            repository = ghapi.get_repo(repo)
            logger.debug(f"Successfully got repository: {repository.full_name}")
        except Exception:
            error_embed = discord.Embed(
                title="Error",
                description="Repository not found.",
                color=discord.Color.red(),
            )
            logger.error(f"Error getting repository: {repo}")
            await interaction.response.send_message(embed=error_embed)
            return

        embed = discord.Embed(
            title=repository.full_name,
            description="[View on GitHub]({})".format(repository.html_url),
            color=discord.Color.green(),
        )

        embed.set_thumbnail(url=repository.owner.avatar_url)

        embed.add_field(name="Stars", value=repository.stargazers_count)
        embed.add_field(name="Watchers", value=repository.watchers_count)
        embed.add_field(name="Language", value=repository.language)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="user", description="Get information about a GitHub user."
    )
    async def gh_user(self, interaction: discord.Interaction, username: str):
        try:
            user = ghapi.get_user(username)
            logger.debug(f"Successfully got user: {user.login}")
        except Exception:
            error_embed = discord.Embed(
                title="Error",
                description="User not found.",
                color=discord.Color.red(),
            )
            logger.error(f"Error getting user: {username}")
            await interaction.response.send_message(embed=error_embed)
            return

        embed = discord.Embed(
            title=user.login,
            description="[View on GitHub]({})".format(user.html_url),
            color=discord.Color.green(),
        )

        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(
            name="Repos",
            value=f"User has {user.public_repos} - [View](https://github.com/{user.login}?tab=repositories)",
        )
        embed.add_field(name="Followers", value=user.followers)
        embed.add_field(name="Following", value=user.following)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Github(bot))
