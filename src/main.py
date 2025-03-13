import dotenv
import discord
import os
from discord.ext import commands
from loguru import logger


class DunnoBot(commands.Bot):
    def __recurse_cogs(self, path: str):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    yield os.path.join(root, file)
                elif os.path.isdir(file):
                    yield from self.__recurse_cogs(file)

    async def setup_hook(self):
        for file in self.__recurse_cogs("src/exts"):
            path = file.replace("/", ".").replace("\\", ".")[:-3]
            logger.debug(f"Loading extension {path}")
            await self.load_extension(path.replace("src.", "").replace(".py", ""))
        return await super().setup_hook()


def main():
    try:
        dotenv.load_dotenv()
    except FileNotFoundError:
        logger.critical("No .env file found!")
        return

    bot = DunnoBot(command_prefix="...", intents=discord.Intents.none())

    bot.run(os.getenv("TOKEN"), log_handler=None)


if __name__ == "__main__":
    main()
